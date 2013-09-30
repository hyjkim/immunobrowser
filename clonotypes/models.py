from django.db import models
from samples.models import Sample
from utils.text_manipulation import convert
import csv
from utils.utils import sub_dict_remove_strict
from django.db.models.query import QuerySet
from django.db.models import Sum, Min, Max

# Create your models here.

# needed for South compatibility

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^coop\.utils\.fields\.MultiSelectField"])


# Example Model

TYPES = ((1, 'Productive'),
        (2, 'Out of frame'),
        (3, 'Has Stop'),
         )

class AminoAcidQuerySet(QuerySet):
    def search(self, terms):
        from django.db.models import Q
        import operator
        terms = [term.upper() for term in terms]
        qgroup = reduce(operator.or_,
            [Q(**{'sequence__contains': term}) for term in terms])
        return self.filter(qgroup)

class AminoAcidManager(models.Manager):
    def get_query_set(self):
        return AminoAcidQuerySet(self.model)
    def __getattr__(self, attr, *args):
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)

class AminoAcid(models.Model):
    sequence = models.CharField(max_length=300)
    objects = AminoAcidManager()

class RecombinationQuerySet(QuerySet):
    def search(self, terms):
        from django.db.models import Q
        import operator
        terms = [term.upper() for term in terms]
        qgroup = reduce(operator.or_,
            [Q(**{'nucleotide__contains': term}) for term in terms])
        return self.filter(qgroup)

class RecombinationManager(models.Manager):
    def get_query_set(self):
        return RecombinationQuerySet(self.model)
    def __getattr__(self, attr, *args):
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)

class Recombination(models.Model):
    '''
    Stores a DNA-level recombination of a TCR.
    '''
    nucleotide = models.CharField(max_length=300)
    v_family_name = models.CharField(max_length=100)
    v_gene_name = models.CharField(max_length=100)
    v_ties = models.CharField(max_length=500)
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

    objects = RecombinationManager()

    @staticmethod
    def functionality_states():
        return list(Recombination.objects.values_list('sequence_status', flat=True).distinct())

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

        # format j gene
        nucleotide_html = '<span class="j_gene">%s</span>' % nucleotide[
            self.j_index:]

        # format n1 region
        if self.n1_index > 0:
            nucleotide_html = ('<span class="n1_additions">%s</span>'
                               % nucleotide[self.n1_index:self.j_index]) + \
                nucleotide_html
        # exclude n1 region
        else:
            self.n1_index = self.j_index

        # format d region
        if self.d_index > 0:
            nucleotide_html = ('<span class="d_gene">%s</span>' %
                               nucleotide[self.d_index:self.n1_index]) + \
                nucleotide_html
        # exclude d region
        else:
            self.d_index = self.n1_index

        # format n2 region
        if self.n2_index > 0:
            nucleotide_html = ('<span class="n2_additions">%s</span>' %
                               nucleotide[self.n2_index:self.d_index]) + \
                nucleotide_html
        # exclude n2 region
        else:
            self.n2_index = self.d_index

        # format v region
        nucleotide_html = ('<span class="v_gene">%s</span>' %
                           nucleotide[:self.n2_index]) + \
            nucleotide_html

        # wrap sequence in a span
        nucleotide_html = '<span class="nucleotide">%s</span>' % nucleotide_html

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
#        num_to_insert = 100
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
    max_copy = models.IntegerField(null=True)
    min_length = models.IntegerField(null=True)
    max_length = models.IntegerField(null=True)
    norm_factor = models.FloatField(null=True)
    v_family_name = models.CharField(max_length=100, null=True)
    j_gene_name = models.CharField(max_length=100, null=True)
#    functionality = MultiSelectField(max_length=250, blank=True, choices=TYPES)

    def css_class(self):
        '''
        Returns a string that represents a class to be used in css.
        Method is used when applicable to encourage consistency in clonofilter
        identification.
        '''
        return "cf-"+str(self.id)


    def save(self, *args, **kwargs):
        if self.norm_factor is None:
            size = self.size()
            if size is not None:
                self.norm_factor = float(size)
        if self.min_copy is None:
            min_copy = self.get_clonotypes().aggregate(Min('copy'))['copy__min']
            if min_copy is not None:
                self.min_copy = min_copy
        if self.max_copy is None:
            max_copy = self.get_clonotypes().aggregate(Max('copy'))['copy__max']
            if max_copy is not None:
                self.max_copy = max_copy
        if self.min_length is None:
            min_length = self.get_clonotypes().aggregate(Min('recombination__cdr3_length'))['recombination__cdr3_length__min']
            if min_length is not None:
                self.min_length = min_length
        if self.max_length is None:
            max_length = self.get_clonotypes().aggregate(Max('recombination__cdr3_length'))['recombination__cdr3_length__max']
            if max_length is not None:
                self.max_length = max_length

        super(ClonoFilter, self).save(*args, **kwargs)

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
        cf_dict['norm_factor'] = cf.size()
        cf_dict['min_copy'] = cf.get_clonotypes().aggregate(Min('copy'))['copy__min']
        cf_dict['max_copy'] = cf.get_clonotypes().aggregate(Max('copy'))['copy__max']
        cf_dict['min_length'] = cf.get_clonotypes().aggregate(Min('recombination__cdr3_length'))['recombination__cdr3_length__min']
        cf_dict['max_length'] = cf.get_clonotypes().aggregate(Max('recombination__cdr3_length'))['recombination__cdr3_length__max']
        cf_dict['j_gene_name'] = ''
        cf_dict['v_family_name'] = ''
        del cf_dict['id']

        cf, created = ClonoFilter.objects.get_or_create(**cf_dict)

        return cf

    def update(self, filter_dict):
        '''
        Given a dictionary of filter conditions, get current conditions
        of current filter, merge with new conditions and return
        a new clonofilter.
        '''
        from django.forms.models import model_to_dict
        this_dict = model_to_dict(self)
        this_dict.update(filter_dict)
        this_dict['sample'] = self.sample
        this_dict.pop("id", None)
        cf, created = ClonoFilter.objects.get_or_create(**this_dict)
        return cf, created

    def get_clonotypes(self):
        ''' Takes in a clonofilter object and returns a queryset '''
        from django.db.models import Q

        # first add the sample id to the query
        query = Q(sample=self.sample)

        queries = []
        if self.min_copy > 0:
            queries.append(Q(copy__gte=self.min_copy))
        if self.max_copy > 0:
            queries.append(Q(copy__lte=self.max_copy))
        if self.min_length > 0:
            queries.append(Q(recombination__cdr3_length__gte=self.min_length))
        if self.max_length > 0:
            queries.append(Q(recombination__cdr3_length__lte=self.max_length))
        if self.v_family_name:
            queries.append(Q(recombination__v_family_name=self.v_family_name))
        if self.j_gene_name:
            queries.append(Q(recombination__j_gene_name=self.j_gene_name))

        for item in queries:
            query.add(item, Q.AND)

        clonotype_queryset = Clonotype.objects.filter(query)
        return clonotype_queryset

    def get_recombinations(self):
        clonotypes = self.get_clonotypes()
        recombinations = Recombination.objects.filter(
            id__in=clonotypes.values('recombination_id'))
        return recombinations

    def count(self):
        '''
        Returns the number of recombinations in a clonofilter
        '''
        return self.get_clonotypes().count()

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
        copy_sum = self.get_clonotypes().aggregate(Sum('copy'))
        return copy_sum['copy__sum']

    def functionality_dict(self):
        '''
        Returns a dict with status as a key and normalized count as a value
        '''
        from django.db.models import Sum
        returnable = {}
        total = 0
        filtered_query_set = self.get_clonotypes()
        functionality_counts = filtered_query_set.values(
            'recombination__sequence_status').annotate(Sum('copy'))
#        for state in Recombination.functionality_states():
#            if state in functionality_counts:
#                pass
        for functionality_count in functionality_counts:
            subtotal = functionality_count['copy__sum']
            returnable[functionality_count['recombination__sequence_status']
                       ] = subtotal
            total += subtotal

        for key, value in returnable.iteritems():
            returnable[key] = 1.0 * value / total
        return returnable

    def j_usage_dict(self):
        '''
        Return a dictionary indexed by j_gene name with values equal to the
        usage of each j_gene within the sample
        '''
        from django.db.models import Sum
        returnable = {}
        # Get set of names in DB
#        j_family_names = Recombination.j_gene_names()
        # Use queryset filtered by values in clonofilter
        filtered_query_set = self.get_clonotypes()
        # Return the sums of each v family
        j_usage_values = filtered_query_set.values(
            'recombination__j_gene_name').annotate(Sum('copy'))
        # Transform list of dicts into single dict
        for sum_dict in j_usage_values:
            if self.norm_factor:
                returnable[sum_dict['recombination__j_gene_name']
                           ] = sum_dict['copy__sum'] / float(self.norm_factor)
            else:
                returnable[sum_dict[
                    'recombination__j_gene_name']] = sum_dict['copy__sum']

        return returnable

    def v_usage_dict(self):
        '''
        Return a dictionary indexed by v_family name with values equal to the
        usage of each v_family within the sample
        '''
        from django.db.models import Sum
        returnable = {}
        # Get set of names in DB
#        v_family_names = Recombination.v_family_names()
        # Use queryset filtered by values in clonofilter
        filtered_query_set = self.get_clonotypes()
        # Return the sums of each v family
        v_usage_values = filtered_query_set.values(
            'recombination__v_family_name').annotate(Sum('copy'))
        # Transform list of dicts into single dict
        for sum_dict in v_usage_values:
            if self.norm_factor:
                returnable[sum_dict['recombination__v_family_name']
                           ] = sum_dict['copy__sum'] / float(self.norm_factor)
            else:
                returnable[sum_dict[
                    'recombination__v_family_name']] = sum_dict['copy__sum']

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
                returnable[v_family][j_gene] = sum_dict[
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
            v_index = v_family_names.index(
                sum_dict['recombination__v_family_name'])
            j_index = j_gene_names.index(
                sum_dict['recombination__j_gene_name'])
            if self.norm_factor:
                returnable[v_index][j_index] = sum_dict[
                    'copy__sum'] / float(self.norm_factor)
            else:
                returnable[v_index][j_index] = sum_dict['copy__sum']

        return returnable

    def cdr3_length_sum_d3(self):
        '''
        Takes in a clonofilter and returns an array of dicts.
        Each dict contains a cdr3 length, sample, and frequency
        '''
        from django.db.models import Sum
        returnable = []
        counts = self.get_clonotypes().values(
            'recombination__cdr3_length').annotate(Sum('copy')).order_by('recombination__cdr3_length')

        for index, sum_counts in enumerate(counts):
            if self.norm_factor:
                freq = sum_counts['copy__sum'] / float(self.norm_factor)
                returnable.append( {
                    'length': sum_counts['recombination__cdr3_length'],
                    'freq': freq,
                    'cfid': self.id,
                    })
            else:
                returnable.append( {
                    'length': sum_counts['recombination__cdr3_length'],
                    'freq': sum_counts['copy__sum'],
                    'cfid': self.id,
                    })

        return returnable


    def cdr3_length_sum(self):
        ''' Takes in a clonofilter and returns a nested list of cdr3_length
        and the number of coutns. Used in matplotlib'''
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

class ClonoFilter2(models.Model):
    '''
    ClonoFilter2 should store filters as a serialized dictionary. This
    has a distinct advantage over the original ClonoFilter in that the model
    does not need to be updated for every existing class
    '''

    sample = models.ForeignKey(Sample)
    valid_filter = {
                    'min copy':'copy',
    }

    def get_clonotypes(self):
        from django.db.models import Q
        query = Q(sample=self.sample)
        clonotype_queryset = Clonotype.objects.filter(query)
        return clonotype_queryset

    def __init__(self, *args, **kwargs):
        pass
