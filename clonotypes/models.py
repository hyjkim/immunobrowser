from django.db import models
from samples.models import Sample
from utils.text_manipulation import convert
import csv
from utils.utils import sub_dict_remove_strict
from django.db.models.query import QuerySet
from django.db.models import Sum, Min, Max
from django.utils.safestring import mark_safe
import datetime

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

    def colorize(self):
        '''
        Given a protein sequence, wrap each amino acid
        in a span that colorizes it
        '''
        COLORS = {
            'W': 'blue',
            'L': 'blue',
            'V': 'blue',
            'I': 'blue',
            'M': 'blue',
            'F': 'blue',
            'A': 'blue',
            'C': 'blue',
            'K': 'red',
            'R': 'red',
            'T': 'green',
            'S': 'green',
            'N': 'green',
            'Q': 'green',
            'C': 'pink',
            'D': 'magenta',
            'E': 'magenta',
            'G': 'orange',
            'H': 'cyan',
            'Y': 'cyan',
            'P': 'yellow',
        }
        color_seq = ''
#        print self.sequence
        for aa in self.sequence:
            if aa in COLORS:
                color_seq += '<span class="aa-%s">%s</span>' % (COLORS[aa], aa)
            else:
                color_seq += aa
        return mark_safe(color_seq)


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
    v_gene_name = models.CharField(max_length=100)
    v_ties = models.CharField(max_length=500, blank=True, null=True)
    d_gene_name = models.CharField(max_length=100)
    d_ties = models.CharField(max_length=100, blank=True, null=True)
    j_gene_name = models.CharField(max_length=100)
    j_ties = models.CharField(max_length=100, blank=True, null=True)
    sequence_status = models.CharField(max_length=100)
    v_deletion = models.IntegerField(blank=True, null=True)
    d5_deletion = models.IntegerField(blank=True, null=True)
    d3_deletion = models.IntegerField(blank=True, null=True)
    j_deletion = models.IntegerField(blank=True, null=True)
    vd_insertion = models.IntegerField()
    dj_insertion = models.IntegerField()
    v_end = models.IntegerField()
    d_start = models.IntegerField()
    d_end = models.IntegerField()
    j_start = models.IntegerField()
    cdr3_length = models.IntegerField()
    amino_acid = models.ForeignKey(AminoAcid, blank=True, null=True)

    objects = RecombinationManager()

    @staticmethod
    def functionality_states():
        return list(Recombination.objects.values_list('sequence_status', flat=True).distinct())

    @staticmethod
    def v_gene_names():
        return list(Recombination.objects.values_list('v_gene_name', flat=True).distinct())

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

        nucleotide = str(self.nucleotide)

        # format j gene
        nucleotide_html = '<span class="j_gene">%s</span>' % nucleotide[
            self.j_start:]

        # format dj region
        if not self.d_end + 1 is self.j_start:
            nucleotide_html = ('<span class="n1_additions">%s</span>'
                               % nucleotide[self.d_end:self.j_start]) + \
                nucleotide_html

        # format d region
        if not self.d_start + 1 is self.d_end:
            nucleotide_html = ('<span class="d_gene">%s</span>' %
                               nucleotide[self.d_start:self.d_end]) + \
                nucleotide_html

        # format n2 region
        if not self.v_end + 1 is self.d_start:
            nucleotide_html = ('<span class="n2_additions">%s</span>' %
                               nucleotide[self.v_end:self.d_start]) + \
                nucleotide_html

        # format v region
        nucleotide_html = ('<span class="v_gene">%s</span>' %
                           nucleotide[:self.v_end]) + \
            nucleotide_html

        # wrap sequence in a span
        nucleotide_html = '<span class="nucleotide">%s</span>' % nucleotide_html

        nucleotide_html = mark_safe(nucleotide_html)
        return nucleotide_html


class Clonotype(models.Model):
    sample = models.ForeignKey(Sample)

    frequency = models.FloatField()
    count = models.IntegerField()
    recombination = models.ForeignKey(Recombination)

    @staticmethod
    def import_mitcr(sample, filename):
        headers = None
        reader = csv.reader(open(filename, 'r'), delimiter="\t")

        start = datetime.datetime.now()

        for row in reader:
            if reader.line_num % 1000 == 0:
                elapsed =  datetime.datetime.now() - start
                print "%s records processed in %s seconds (%s records/min)" % (reader.line_num, elapsed.seconds, (reader.line_num / elapsed.seconds * 60))

            if reader.line_num == 1:
                headers = row
            else:
                line_dict = {}
                line_dict = dict(zip(headers, row))

                # set the default v family
                v_segments = line_dict['V segments'].split(", ")
                v_gene_name = v_segments[0]
                if len(v_segments) > 1:
                    v_ties = line_dict['V segments']
                else:
                    v_ties = None

                d_segments = line_dict['D segments'].split(", ")
                d_gene_name = d_segments[0]
                if len(d_segments) > 1:
                    d_ties = line_dict['D segments']
                else:
                    d_ties = None

                j_segments = line_dict['J segments'].split(", ")
                j_gene_name = j_segments[0]
                if len(j_segments) > 1:
                    j_ties = line_dict['J segments']
                else:
                    j_ties = None

                # check sequence status
                sequence_status = None
                if '*' in line_dict['CDR3 amino acid sequence']:
                    sequence_status = "Has stop"
                elif '~' in line_dict['CDR3 amino acid sequence']:
                    sequence_status = "Out of frame"
                else:
                    sequence_status = "Productive"

                # compute cdr3 length
                cdr3_length = len(line_dict['CDR3 nucleotide sequence'])

                aa = None

                if sequence_status is "Productive":
                    aa, created = AminoAcid.objects.get_or_create(
                        sequence=line_dict['CDR3 amino acid sequence'])

                r, created = Recombination.objects.get_or_create(
                    nucleotide=line_dict['CDR3 nucleotide sequence'],
                    v_gene_name=v_gene_name,
                    v_ties=v_ties,
                    d_gene_name=d_gene_name,
                    d_ties=d_ties,
                    j_gene_name=j_gene_name,
                    j_ties=j_ties,
                    sequence_status=sequence_status,
                    v_deletion=None,
                    d5_deletion=None,
                    d3_deletion=None,
                    j_deletion=None,
                    vd_insertion=line_dict['VD insertions'],
                    dj_insertion=line_dict['DJ insertions'],
                    v_end=line_dict['Last V nucleotide position '],
                    d_start=line_dict['First D nucleotide position'],
                    d_end=line_dict['Last D nucleotide position'],
                    j_start=line_dict['First J nucleotide position'],
                    cdr3_length=cdr3_length,
                    amino_acid=aa)

                Clonotype.objects.create(
                        sample=sample,
                        frequency=line_dict['Percentage'],
                        count=line_dict['Read count'],
                        recombination=r
                        )

    @staticmethod
    def import_adaptive(sample, filename):
        headers = None
        reader = csv.reader(open(filename, 'r'), delimiter="\t")

        for row in reader:
            if reader.line_num == 1:
                headers = row
            else:
                line_dict = {}
                line_dict = dict(zip(headers, row))

                aa = None

                if line_dict['aminoAcid'] is not '':
                    aa, created = AminoAcid.objects.get_or_create(
                        sequence=line_dict['aminoAcid'])

                # Preprocess lines to fit with our definitions
                if line_dict['VGeneName'] is '(undefined)':
                    line_dict['VGeneName'] = line_dict['VTies'].split(", ")[0]
                if line_dict['JGeneName'] is '(undefined)':
                    line_dict['JGeneName'] = line_dict['JTies'].split(", ")[0]
                if line_dict['n1Index'] <= 0:
                    line_dict['n1Index'] = line_dict['JIndex']
                if line_dict['n2Index'] <= 0:
                    line_dict['n2Index'] = line_dict['DIndex']
                line_dict['DIndex'] = int(line_dict['DIndex']) + 1
                line_dict['JIndex'] = int(line_dict['JIndex']) + 1

                r, created = Recombination.objects.get_or_create(
                    nucleotide=line_dict['nucleotide'],
                    v_gene_name=line_dict['VGeneName'],
                    v_ties=line_dict['VTies'],
                    d_gene_name=line_dict['DGeneName'],
                    d_ties=None,
                    j_gene_name=line_dict['JGeneName'],
                    j_ties=line_dict['JTies'],
                    sequence_status=line_dict['sequenceStatus'],
                    v_deletion=line_dict['VDeletion'],
                    d5_deletion=line_dict['d5Deletion'],
                    d3_deletion=line_dict['d3Deletion'],
                    j_deletion=line_dict['JDeletion'],
                    vd_insertion=line_dict['n2Insertion'],
                    dj_insertion=line_dict['n1Insertion'],
                    v_end=line_dict['n2Index'],
                    d_start=line_dict['DIndex'],
                    d_end=line_dict['n1Index'],
                    j_start=line_dict['JIndex'],
                    cdr3_length=line_dict['cdr3Length'],
                    amino_acid=aa)

                Clonotype.objects.create(
                        sample=sample,
                        frequency=line_dict['normalizedFrequency'],
                        count=line_dict['normalizedCopy'],
                        recombination=r)


    @staticmethod
    def import_tsv_old(sample, filename):
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
    min_count = models.IntegerField(null=True)
    max_count = models.IntegerField(null=True)
    min_length = models.IntegerField(null=True)
    max_length = models.IntegerField(null=True)
    norm_factor = models.FloatField(null=True)
    v_gene_name = models.CharField(max_length=100, null=True)
    j_gene_name = models.CharField(max_length=100, null=True)
#    functionality = MultiSelectField(max_length=250, blank=True, choices=TYPES)

    def css_class(self):
        '''
        Returns a string that represents a class to be used in css.
        Method is used when applicable to encourage consistency in clonofilter
        identification.
        '''
        return "cf-" + str(self.id)

    def save(self, *args, **kwargs):
        if self.norm_factor is None:
            size = self.size()
            if size is not None:
                self.norm_factor = float(size)
        if self.min_count is None:
            min_count = self.get_clonotypes(
            ).aggregate(Min('count'))['count__min']
            if min_count is not None:
                self.min_count = min_count
        if self.max_count is None:
            max_count = self.get_clonotypes(
            ).aggregate(Max('count'))['count__max']
            if max_count is not None:
                self.max_count = max_count
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
        cf_dict['min_count'] = cf.get_clonotypes(
        ).aggregate(Min('count'))['count__min']
        cf_dict['max_count'] = cf.get_clonotypes(
        ).aggregate(Max('count'))['count__max']
        cf_dict['min_length'] = cf.get_clonotypes().aggregate(Min(
            'recombination__cdr3_length'))['recombination__cdr3_length__min']
        cf_dict['max_length'] = cf.get_clonotypes().aggregate(Max(
            'recombination__cdr3_length'))['recombination__cdr3_length__max']
        cf_dict['j_gene_name'] = ''
        cf_dict['v_gene_name'] = ''
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
        if self.min_count > 0:
            queries.append(Q(count__gte=self.min_count))
        if self.max_count > 0:
            queries.append(Q(count__lte=self.max_count))
        if self.min_length > 0:
            queries.append(Q(recombination__cdr3_length__gte=self.min_length))
        if self.max_length > 0:
            queries.append(Q(recombination__cdr3_length__lte=self.max_length))
        if self.v_gene_name:
            queries.append(Q(recombination__v_gene_name=self.v_gene_name))
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

    def get_amino_acids(self):
        '''
        Returns a queryset of amino acids
        '''
        amino_acids = AminoAcid.objects.filter(
            recombination__clonotype__in=self.get_clonotypes())
        return amino_acids

    def amino_count(self):
        '''
        Returns the number of unique amino acid sequences in a clonofilter
        '''
        return self.get_amino_acids().count()

    def count(self):
        '''
        Returns the number of recombinations in a clonofilter
        '''
        return self.get_clonotypes().count()

    def norm_size(self):
        '''
        Returns the normalized sum of 'count' given a clonofilter
        '''
        norm_sum = self.size() / self.norm_factor
        return norm_sum

    def size(self):
        '''
        Returns the sum of 'count' given a clonofilter
        '''
        count_sum = self.get_clonotypes().aggregate(Sum('count'))
        return count_sum['count__sum']

    def functionality_dict(self):
        '''
        Returns a dict with status as a key and normalized count as a value
        '''
        from django.db.models import Sum
        returnable = {}
        total = 0
        filtered_query_set = self.get_clonotypes()
        functionality_counts = filtered_query_set.values(
            'recombination__sequence_status').annotate(Sum('count'))
#        for state in Recombination.functionality_states():
#            if state in functionality_counts:
#                pass
        for functionality_count in functionality_counts:
            subtotal = functionality_count['count__sum']
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
            'recombination__j_gene_name').annotate(Sum('count'))
        # Transform list of dicts into single dict
        for sum_dict in j_usage_values:
            if self.norm_factor:
                returnable[sum_dict['recombination__j_gene_name']
                           ] = sum_dict['count__sum'] / float(self.norm_factor)
            else:
                returnable[sum_dict[
                    'recombination__j_gene_name']] = sum_dict['count__sum']

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
            'recombination__v_gene_name').annotate(Sum('count'))
        # Transform list of dicts into single dict
        for sum_dict in v_usage_values:
            if self.norm_factor:
                returnable[sum_dict['recombination__v_gene_name']
                           ] = sum_dict['count__sum'] / float(self.norm_factor)
            else:
                returnable[sum_dict[
                    'recombination__v_gene_name']] = sum_dict['count__sum']

        return returnable

    def freq_hist(self):
        '''
        Returns 2d array where the first column is the histogram bin and the
        second column is the observed frequency
        '''
        # set 10 bins on a log scale
        pass

    def top_clones(self, num_clones=100):
        '''
        Returns the frequencies of the top clones. If no number of clones to
        return is specified, returns 100 by default
        '''
        return(self.get_clonotypes().order_by("-count")[:num_clones])

    def entropy(self):
        '''
        Returns the shannon entropy of a clonofilter where probabiliities
        are observed frequencies.
        '''
        from scipy.stats import entropy
        # Get normalization factor
        cf_sum = self.size()

        # Get all clonofilter read counts
        freqs = [float(count) / cf_sum for count in self.get_clonotypes(
        ).values_list('count', flat=True)]
        return entropy(freqs)

    def vj_counts_dict(self):
        ''' Takes in a clonofilter and returns a nested dict of v_family_name
        index in v_family_names, j_gene_name index in j_gene_names
        and sum of count.

        dict should be indexed by:
            dict['v_family']['j_gene'] = count
        '''
        from collections import defaultdict
        from django.db.models import Sum

        returnable = defaultdict(lambda: defaultdict(lambda: .0))
        filtered_query_set = self.get_clonotypes()
        # Returns a list of dicts, each dict contains a v gene, j gene and a
        # sum of count
        vj_pairs = filtered_query_set.values(
            'recombination__v_gene_name', 'recombination__j_gene_name').annotate(Sum('count'))

        for sum_dict in vj_pairs:
            v_family = sum_dict['recombination__v_gene_name']
            j_gene = sum_dict['recombination__j_gene_name']

            if self.norm_factor:
                returnable[v_family][j_gene] = sum_dict[
                    'count__sum'] / float(self.norm_factor)
            else:
                returnable[v_family][j_gene] = sum_dict['count__sum']

        return returnable

    def vj_counts(self):
        ''' Takes in a clonofilter and returns a nested list of v_gene_name
        index in v_gene_names, j_gene_name index in j_gene_names
        and sum of count '''
        from django.db.models import Sum

        filtered_query_set = self.get_clonotypes()
        # Returns a list of dicts, each dict contains a v gene, j gene and a
        # sum of count
        vj_pairs = filtered_query_set.values(
            'recombination__v_gene_name', 'recombination__j_gene_name').annotate(Sum('count'))
        # Get v and j gene names in a list
        v_gene_names = Recombination.v_gene_names()
        j_gene_names = Recombination.j_gene_names()

        # Initialize an empty list the size of v_gene_names and j_gene_names
        returnable = [([0] * len(j_gene_names)) for i in range(len(
            v_gene_names))]

        for sum_dict in vj_pairs:
            v_index = v_gene_names.index(
                sum_dict['recombination__v_gene_name'])
            j_index = j_gene_names.index(
                sum_dict['recombination__j_gene_name'])
            if self.norm_factor:
                returnable[v_index][j_index] = sum_dict[
                    'count__sum'] / float(self.norm_factor)
            else:
                returnable[v_index][j_index] = sum_dict['count__sum']

        return returnable

    def cdr3_length_sum_d3(self):
        '''
        Takes in a clonofilter and returns an array of dicts.
        Each dict contains a cdr3 length, sample, and frequency
        '''
        from django.db.models import Sum
        returnable = []
        counts = self.get_clonotypes().values(
            'recombination__cdr3_length').annotate(Sum('count')).order_by('recombination__cdr3_length')

        for index, sum_counts in enumerate(counts):
            if self.norm_factor:
                freq = sum_counts['count__sum'] / float(self.norm_factor)
                returnable.append({
                    'length': sum_counts['recombination__cdr3_length'],
                    'freq': freq,
                    'cfid': self.id,
                })
            else:
                returnable.append({
                    'length': sum_counts['recombination__cdr3_length'],
                    'freq': sum_counts['count__sum'],
                    'cfid': self.id,
                })

        return returnable

    def cdr3_length_sum(self):
        ''' Takes in a clonofilter and returns a nested list of cdr3_length
        and the number of coutns. Used in matplotlib'''
        from django.db.models import Sum
        returnable = []
        counts = self.get_clonotypes().values(
            'recombination__cdr3_length').annotate(Sum('count')).order_by('recombination__cdr3_length')

        for index, sum_counts in enumerate(counts):
            if self.norm_factor:
                returnable.append([sum_counts['recombination__cdr3_length'],
                                   sum_counts['count__sum'] / float(self.norm_factor)])
            else:
                returnable.append([sum_counts['recombination__cdr3_length'],
                                   sum_counts['count__sum']])

        return returnable


class ClonoFilter2(models.Model):
    '''
    ClonoFilter2 should store filters as a serialized dictionary. This
    has a distinct advantage over the original ClonoFilter in that the model
    does not need to be updated for every existing class
    '''

    sample = models.ForeignKey(Sample)
    valid_filter = {
        'min count': 'count',
    }

    def get_clonotypes(self):
        from django.db.models import Q
        query = Q(sample=self.sample)
        clonotype_queryset = Clonotype.objects.filter(query)
        return clonotype_queryset

    def __init__(self, *args, **kwargs):
        pass
