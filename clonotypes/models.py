from django.db import models
from samples.models import Sample
from utils.text_manipulation import convert
import csv

# Create your models here.


class Clonotype(models.Model):
    sample = models.ForeignKey(Sample)
    sequence_id = models.CharField(max_length=100)
    container = models.CharField(max_length=100)
    nucleotide = models.CharField(max_length=300)
    amino_acid = models.CharField(max_length=100)
    normalized_frequency = models.FloatField()
    normalized_copy = models.IntegerField()
    raw_frequency = models.FloatField()
    copy = models.IntegerField()
    cdr3_length = models.IntegerField()
    v_family_name = models.CharField(max_length=100)
    v_gene_name = models.CharField(max_length=100)
    v_ties = models.CharField(max_length=100)
    d_gene_name = models.CharField(max_length=100)
    j_gene_name = models.CharField(max_length=100)
    j_ties = models.CharField(max_length=100)
    v_deletion = models.IntegerField()
    d5_deletion = models.IntegerField()
    d3_deletion = models.IntegerField()
    j_deletion = models.IntegerField()
    n2_insertion = models.IntegerField()
    n1_insertion = models.IntegerField()
    sequence_status = models.CharField(max_length=100)
    v_index = models.IntegerField()
    n1_index = models.IntegerField()
    n2_index = models.IntegerField()
    d_index = models.IntegerField()
    j_index = models.IntegerField()

    @staticmethod
    def import_tsv(sample, filename):
        headers = None
        num_to_insert = 100
        clonotype_list = []
        reader = csv.reader(open(filename, 'r'), delimiter="\t")

        for row in reader:
            if reader.line_num == 1:
                headers = row
                headers = map(convert, headers)
            else:
                clonotype = {}
                clonotype = dict(zip(headers, row))
                if(clonotype['normalized_frequency'] == ''):
                    raise Exception('Normalized_frequency cannot be null')
                clonotype_list.append(Clonotype(sample=sample, **clonotype))
                if len(clonotype_list) > num_to_insert:
                    Clonotype.objects.bulk_create(clonotype_list)
                    clonotype_list = []

        Clonotype.objects.bulk_create(clonotype_list)

    @staticmethod
    def v_family_names():
        return list(Clonotype.objects.values_list('v_family_name', flat=True).distinct())

    @staticmethod
    def j_gene_names():
        return list(Clonotype.objects.values_list('j_gene_name', flat=True).distinct())

    def parsed_nucleotide(self):
        ''' Returns a string of the nucleotide sequence with distinct gene
        regions within spans. Each span has a classname so that it can be
        colored via css

        It is worth noting that n2 additions actually appear before n1 in the
        nucleotide string. This reflects the biology where the dj junction is
        joined before the vj junction'''
        from django.utils.safestring import mark_safe

        nucleotide = str(self.nucleotide)
#        nucleotide_html = '<span class="v_gene">' + nucleotide[:self.n2_index] + '</span>'
#        nucleotide_html += '<span class="n2_additions">' + nucleotide[self.n2_index:self.d_index] + '</span>'
#        nucleotide_html += '<span class="d_gene">' + nucleotide[self.d_index:self.n1_index] + '</span>'
#        nucleotide_html += '<span class="n1_additions">' + nucleotide[self.n1_index:self.j_index] + '</span>'
#        nucleotide_html += '<span class="j_gene">' + nucleotide[self.j_index:] + '</span>'

        nucleotide_html = '<span class="j_gene">%s</span>' % nucleotide[
            self.j_index:]
        if self.n1_index > 0:
            nucleotide_html = ('<span class="n1_additions">%s</span>'
                               % nucleotide[self.n1_index:self.j_index]) + \
                nucleotide_html
        else:
            self.n1_index = self.j_index

        if self.d_index > 0:
            nucleotide_html = ('<span class="d_gene">%s</span>' %
                               nucleotide[self.d_index:self.n1_index]) + \
                nucleotide_html
        else:
            self.d_index = self.n1_index

        if self.n2_index > 0:
            nucleotide_html = ('<span class="n2_additions">%s</span>' %
                               nucleotide[self.n2_index:self.d_index]) + \
                nucleotide_html
        else:
            self.n2_index = self.d_index

        nucleotide_html = ('<span class="v_gene">%s</span>' %
                           nucleotide[:self.n2_index]) + \
            nucleotide_html

        nucleotide_html = mark_safe(nucleotide_html)
        return nucleotide_html


class ClonoFilter(models.Model):
    sample = models.ForeignKey(Sample)
    min_copy = models.IntegerField(null=True)
    min_length = models.IntegerField(null=True)
    max_length = models.IntegerField(null=True)
    norm_factor = models.FloatField(null=True)

    @staticmethod
    def default_from_sample(sample):
        ''' Given a sample, create a clonofilter that uses the default options '''
        from django.forms.models import model_to_dict
        cf = ClonoFilter(**{'sample': sample})
        # The following is my hacky way to grab a default clonofilter
        # with no filter values applied without creating a new object
        # for each request
        cf_dict = model_to_dict(cf)
        cf_dict['sample'] = sample
        del cf_dict['id']

        cf, created = ClonoFilter.objects.get_or_create(**cf_dict)

        return cf


    def get_clonotypes(self):
        ''' Takes in a clonofilter object and returns a queryset '''
        from django.db.models import Q

        # first add the sample id to the query
        query = Q(sample=self.sample)

        queries = []
        if self.min_copy > 0:
            queries.append(Q(copy__gte=self.min_copy))
        if self.min_length > 0:
            queries.append(Q(cdr3_length__gte=self.min_length))
        if self.max_length > 0:
            queries.append(Q(cdr3_length__lte=self.max_length))

        for item in queries:
            query.add(item, Q.AND)

        clonotype_queryset = Clonotype.objects.filter(query)
        return clonotype_queryset

    def vj_counts(self):
        from django.db.models import Sum
        ''' Takes in a clonofilter and returns a nested list of v_family_name
        index in v_family_names, j_gene_name index in j_gene_names
        and sum of copy '''
        filtered_query_set = self.get_clonotypes()
        vj_pairs = filtered_query_set.values(
            'v_family_name', 'j_gene_name').annotate(Sum('copy'))
        v_family_names = Clonotype.v_family_names()
        j_gene_names = Clonotype.j_gene_names()

        returnable = [([0] * len(j_gene_names)) for i in range(len(
            v_family_names))]

        for sum_dict in vj_pairs:
            v_index = v_family_names.index(sum_dict['v_family_name'])
            j_index = j_gene_names.index(sum_dict['j_gene_name'])
            if self.norm_factor:
                returnable[v_index][j_index] = sum_dict[
                    'copy__sum'] / float(self.norm_factor)
            else:
                returnable[v_index][j_index] = sum_dict['copy__sum']

        return returnable

    def cdr3_length_sum(self):
        ''' Takes in a clonofilter and returns a nested list of cdr3_length
        and the number of coutns '''
        from django.db.models import Sum
        returnable = []
        counts = self.get_clonotypes().values(
            'cdr3_length').annotate(Sum('copy')).order_by('cdr3_length')

        for index, sum_counts in enumerate(counts):
            if self.norm_factor:
                returnable.append([sum_counts['cdr3_length'],
                                   sum_counts['copy__sum'] / float(self.norm_factor)])
            else:
                returnable.append([sum_counts['cdr3_length'],
                                   sum_counts['copy__sum']])

        return returnable
