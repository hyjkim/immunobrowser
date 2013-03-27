from django.db import models
from samples.models import Sample
from utils.text_manipulation import convert
import csv
from utils.utils import sub_dict_remove_strict

# Create your models here.


class AminoAcid(models.Model):
    sequence = models.CharField(max_length=300)


class Recombination(models.Model):
    '''
    Stores a DNA-level recombination of a TCR.
    '''
    nucleotide = models.CharField(max_length=300)
    v_family_name = models.CharField(max_length=100)
    v_gene_name = models.CharField(max_length=100)
    v_ties = models.CharField(max_length=100)
    d_gene_name = models.CharField(max_length=100)
    j_gene_name = models.CharField(max_length=100)
    j_ties = models.CharField(max_length=100)
    sequence_status = models.CharField(max_length=100)
    v_deletion = models.IntegerField()
    d5_deletion = models.IntegerField()
    d3_deletion = models.IntegerField()
    j_deletion = models.IntegerField()
    n2_insertion = models.IntegerField()
    n1_insertion = models.IntegerField()
    v_index = models.IntegerField()
    n1_index = models.IntegerField()
    n2_index = models.IntegerField()
    d_index = models.IntegerField()
    j_index = models.IntegerField()
    cdr3_length = models.IntegerField()
    amino_acid = models.ForeignKey(AminoAcid, blank=True, null=True)

    @staticmethod
    def v_family_names():
        return list(Recombination.objects.values_list('v_family_name', flat=True).distinct())

    @staticmethod
    def j_gene_names():
        return list(Recombination.objects.values_list('j_gene_name', flat=True).distinct())

    def parsed_nucleotide(self):
        ''' Returns a string of the nucleotide sequence with distinct gene
        regions within spans. Each span has a classname so that it can be
        colored via css

        It is worth noting that n2 additions actually appear before n1 in the
        nucleotide string. This reflects the biology where the dj junction is
        joined before the vj junction'''
        from django.utils.safestring import mark_safe

        nucleotide = str(self.nucleotide)

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



class Clonotype(models.Model):
    sample = models.ForeignKey(Sample)
    sequence_id = models.CharField(max_length=100)
    container = models.CharField(max_length=100)
    normalized_frequency = models.FloatField()
    normalized_copy = models.IntegerField()
    raw_frequency = models.FloatField()
    copy = models.IntegerField()
    recombination = models.ForeignKey(Recombination)



    @staticmethod
    def import_tsv(sample, filename):
        headers = None
        num_to_insert = 100
#        clonotype_list = []
#        amino_acid_list = []
#        recombination_list = []
        reader = csv.reader(open(filename, 'r'), delimiter="\t")

        recombination_cols = ['nucleotide',
                              'v_family_name',
                              'v_gene_name',
                              'v_ties',
                              'd_gene_name',
                              'j_gene_name',
                              'j_ties',
                              'sequence_status',
                              'v_deletion',
                              'd5_deletion',
                              'd3_deletion',
                              'j_deletion',
                              'n2_insertion',
                              'n1_insertion',
                              'v_index',
                              'n1_index',
                              'n2_index',
                              'd_index',
                              'j_index',
                              'cdr3_length',
                              ]
        amino_acid_cols = ['amino_acid']
        clonotype_cols = [
            'sequence_id',
            'container',
            'normalized_frequency',
            'normalized_copy',
            'raw_frequency',
            'copy',
        ]

        for row in reader:
            if reader.line_num == 1:
                headers = row
                headers = map(convert, headers)
            else:
                line_dict = {}
                line_dict = dict(zip(headers, row))

# split into clonotype, recombination and amino acid dicts
                amino_acid_dict = sub_dict_remove_strict(
                    line_dict, amino_acid_cols)
                recombination_dict = sub_dict_remove_strict(
                    line_dict, recombination_cols)
                clonotype_dict = sub_dict_remove_strict(
                    line_dict, clonotype_cols)

# throw error if any leftover columns
                if line_dict:
                    raise Exception('Unidentified column in file')
                if clonotype_dict['normalized_frequency'] == '':
                    raise Exception('Normalized_frequency cannot be null')
                if not amino_acid_dict['amino_acid'] == '':
                    # Fix discrepancies between column and model fields
                    amino_acid_dict['sequence'] = amino_acid_dict['amino_acid']
                    del amino_acid_dict['amino_acid']
                    aa, created = AminoAcid.objects.get_or_create(
                        **amino_acid_dict)
#                    aa.samples.add(sample)
#                    aa.save()
                    r, created = Recombination.objects.get_or_create(
                        amino_acid=aa, **recombination_dict)
                else:
                    r, created = Recombination.objects.get_or_create(
                        **recombination_dict)
                clonotype_dict['recombination'] = r
                clonotype_dict['sample'] = sample
                Clonotype.objects.create(**clonotype_dict)


class ClonoFilter(models.Model):
    sample = models.ForeignKey(Sample)
    min_copy = models.IntegerField(null=True)
    min_length = models.IntegerField(null=True)
    max_length = models.IntegerField(null=True)
    norm_factor = models.FloatField(null=True, default=1)

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
            queries.append(Q(recombination__cdr3_length__gte=self.min_length))
        if self.max_length > 0:
            queries.append(Q(recombination__cdr3_length__lte=self.max_length))

        for item in queries:
            query.add(item, Q.AND)

        clonotype_queryset = Clonotype.objects.filter(query)
        return clonotype_queryset

    def get_recombinations(self):
        clonotypes = self.get_clonotypes()
        recombinations = Recombination.objects.filter(id__in=clonotypes.values('recombination_id'))
        return recombinations

    def norm_size(self):
        '''
        Returns the normalized sum of 'copy' given a clonofilter
        '''
        norm_sum = self.size() / self.norm_factor
        return norm_sum

    def size(self):
        '''
        Returns the sum of 'copy' given a clonofilter
        '''
        from django.db.models import Sum
        copy_sum = self.get_clonotypes().aggregate(Sum('copy'))
        return copy_sum['copy__sum']

    def j_usage_dict(self):
        '''
        Return a dictionary indexed by j_gene name with values equal to the
        usage of each j_gene within the sample
        '''
        from django.db.models import Sum
        returnable = {}
        # Get set of names in DB
        j_family_names = Recombination.j_gene_names()
        # Use queryset filtered by values in clonofilter
        filtered_query_set = self.get_clonotypes()
        # Return the sums of each v family
        j_usage_values = filtered_query_set.values('recombination__j_gene_name').annotate(Sum('copy'))
        # Transform list of dicts into single dict
        for sum_dict in j_usage_values:
            if self.norm_factor:
                returnable[sum_dict['recombination__j_gene_name']] = sum_dict['copy__sum'] / float(self.norm_factor)
            else:
                returnable[sum_dict['recombination__j_gene_name']] = sum_dict['copy__sum']

        return returnable

    def v_usage_dict(self):
        '''
        Return a dictionary indexed by v_family name with values equal to the
        usage of each v_family within the sample
        '''
        from django.db.models import Sum
        returnable = {}
        # Get set of names in DB
        v_family_names = Recombination.v_family_names()
        # Use queryset filtered by values in clonofilter
        filtered_query_set = self.get_clonotypes()
        # Return the sums of each v family
        v_usage_values = filtered_query_set.values('recombination__v_family_name').annotate(Sum('copy'))
        # Transform list of dicts into single dict
        for sum_dict in v_usage_values:
            if self.norm_factor:
                returnable[sum_dict['recombination__v_family_name']] = sum_dict['copy__sum'] / float(self.norm_factor)
            else:
                returnable[sum_dict['recombination__v_family_name']] = sum_dict['copy__sum']

        return returnable

    def vj_counts_dict(self):
        ''' Takes in a clonofilter and returns a nested dict of v_family_name
        index in v_family_names, j_gene_name index in j_gene_names
        and sum of copy.

        dict should be indexed by:
            dict['v_family']['j_gene'] = count
        '''
        from collections import defaultdict
        from django.db.models import Sum

        returnable = defaultdict(lambda: defaultdict(lambda: .0))
        filtered_query_set = self.get_clonotypes()
        # Returns a list of dicts, each dict contains a v gene, j gene and a
        # sum of copy
        vj_pairs = filtered_query_set.values(
            'recombination__v_family_name', 'recombination__j_gene_name').annotate(Sum('copy'))

        for sum_dict in vj_pairs:
            v_family = sum_dict['recombination__v_family_name']
            j_gene = sum_dict['recombination__j_gene_name']

            if self.norm_factor:
                 returnable[v_family][j_gene] =  sum_dict[
                    'copy__sum'] / float(self.norm_factor)
            else:
                returnable[v_family][j_gene] = sum_dict['copy__sum']

        return returnable

    def vj_counts(self):
        ''' Takes in a clonofilter and returns a nested list of v_family_name
        index in v_family_names, j_gene_name index in j_gene_names
        and sum of copy '''
        from django.db.models import Sum

        filtered_query_set = self.get_clonotypes()
        # Returns a list of dicts, each dict contains a v gene, j gene and a
        # sum of copy
        vj_pairs = filtered_query_set.values(
            'recombination__v_family_name', 'recombination__j_gene_name').annotate(Sum('copy'))
        # Get v and j gene names in a list
        v_family_names = Recombination.v_family_names()
        j_gene_names = Recombination.j_gene_names()

        # Initialize an empty list the size of v_family_names and j_gene_names
        returnable = [([0] * len(j_gene_names)) for i in range(len(
            v_family_names))]

        for sum_dict in vj_pairs:
            v_index = v_family_names.index(sum_dict['recombination__v_family_name'])
            j_index = j_gene_names.index(sum_dict['recombination__j_gene_name'])
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
            'recombination__cdr3_length').annotate(Sum('copy')).order_by('recombination__cdr3_length')

        for index, sum_counts in enumerate(counts):
            if self.norm_factor:
                returnable.append([sum_counts['recombination__cdr3_length'],
                                   sum_counts['copy__sum'] / float(self.norm_factor)])
            else:
                returnable.append([sum_counts['recombination__cdr3_length'],
                                   sum_counts['copy__sum']])

        return returnable
