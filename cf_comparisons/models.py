from django.db import models
from clonotypes.models import ClonoFilter, Recombination
from utils.utils import undefaulted
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import numpy as np
import json


class Comparison(models.Model):
    _clonofilters = models.TextField(null=True, db_column='clonofilters_list')

    def cdr3_length_sums(self):
        '''
        Calls clonofilter model method for all clonofilters in a comparison
        and returns some json friendly stuff.
        '''
        clonofilters = self.clonofilters_all()
        returnable = []
        for cf in clonofilters:
            returnable += cf.cdr3_length_sum_d3()

        return returnable

    def vj_freq(self):
        '''
        Returns a list of lists containing frequences of each
        v_family-j_gene pair and the clonofilter id
        '''
        clonofilters = sorted(self.clonofilters_all())
        vj_counts_dict_dict= dict([(clonofilter.id, clonofilter.vj_counts_dict())
                        for clonofilter in clonofilters])

        v_list = sorted(Recombination.v_family_names())
        j_list = sorted(Recombination.j_gene_names())

        data = []

        # Counts for the scatter plot
        for clonofilter_id, vj_counts_dict in vj_counts_dict_dict.iteritems():
            for v_index, v_family in enumerate(v_list):
                for j_index, j_gene in enumerate(j_list):
                    data_point = []
                    data_point.append(v_list[v_index])
                    data_point.append(j_list[j_index])
                    if vj_counts_dict[v_family][j_gene]:
                        data_point.append(vj_counts_dict[v_family][j_gene])
                    else:
                        data_point.append(0)
                    # Append sample id
                    data_point.append(clonofilter_id);
                    if data_point[2] > 0:
                        data.append(data_point)

        return data

    def freq_hist(self):
        '''
        '''
        pass

    def add_samples(self, samples):
        '''
        Given an array of sample ids, add them to the current comparison
        and then return a new comparison
        '''
        cfs = list(self.clonofilters_all())

        new_cfs = [ClonoFilter.default_from_sample(sample)
                                for sample in samples]

        comparison, created = Comparison.get_or_create_from_clonofilters(
            cfs+new_cfs)

        return comparison


    def update(self, cf_params):
        '''
        Given an array update dicts returns a new comparison.
        Each member of the array is a dict with two keys: 'key' and 'values'
        'key' contains the clonofilter id and 'values' stores a dictionary
        with filter parameters.
        '''
        cfs = self.clonofilters_all()
        colors = self.colors()
        new_colors = {}
        new_cfs = []

        for cf in cfs:
            if(cf.id in cf_params):
                new_cf, created = cf.update(cf_params[cf.id])
                new_cfs.append(new_cf)
                new_colors[new_cf.id] = colors[cf.id]
            else:
                new_cfs.append(cf)
                new_colors[cf.id] = colors[cf.id]
        comp, created = Comparison.get_or_create_from_clonofilters(new_cfs)

        if created:
            comp.set_colors(new_colors)

        return comp


    def rgba_colors(self, *args):
        '''
        Returns colors in rgba format for use in css.
        Takes in a float as an optional value for opacity.
        Otherwise opacity defaults to 1
        '''
        try:
            opacity = args[0]
        except:
            opacity = 1

        cf_colors = self.colors()
        for cf, color in cf_colors.iteritems():
            color = hex_to_rgb(color)
            color.append(opacity)
            cf_colors[cf] = 'rgba(' + ', '.join([str(v) for v in color]) + ')'
        return cf_colors


    def colors(self):
        '''
        Returns a dict where keys are clonofilter ids and colors are hex strings.
        If a clonofilter does not have a color, one is assigned automagically
        '''
        from matplotlib import cm
        from matplotlib.colors import rgb2hex
        returnable = {}
        cfs = self.clonofilters_all()
        cf_colors = ComparisonColor.objects.filter(comparison=self, clonofilter__in=cfs).all()
        for cf_color in cf_colors:
            try:
                returnable[cf_color.clonofilter.id] = cf_color.color
            except:
                returnable[cf_color.clonofilter.id] = None

        # color logic
        need_color = list(set([cf.id for cf in cfs]) - set(returnable.keys()))

        if len(need_color):
            colormap = cm.get_cmap('gist_rainbow')
            colors = [rgb2hex(colormap(1. * i / len(need_color)))
                        for i in range(len(need_color))]
            new_colors = dict(zip(need_color,colors))
            self.set_colors(new_colors)
            returnable.update(new_colors)

        return returnable

    def set_colors(self, color_dict):
        '''
        Given a dictionary where key: clonofilter id and value: color represented in hex
        prefixed by # (ie #000000), update all values in the database.
        '''
        for clonofilter_id, color in color_dict.iteritems():
            clonofilter = ClonoFilter.objects.get(id=clonofilter_id)
            cc, created = ComparisonColor.objects.get_or_create(
                comparison=self, clonofilter=clonofilter)
            cc.color = color
            cc.save()

    def filter_forms_dict(self):
        '''
        Returns a dict of filter forms indexed by clonofilters
        in a comparison
        '''
        from clonotypes.forms import ClonoFilterForm

        clonofilters = self.clonofilters_all()
        filter_forms = {}
        for clonofilter in clonofilters:
            filter_forms[clonofilter] = ClonoFilterForm(initial=ClonoFilter.objects.filter(
                id=clonofilter.id).values()[0], prefix=str(clonofilter.id))
        return filter_forms

    def filter_forms(self):
        '''
        Returns a list of tuples including clonofilter and filter form
        for individual clonofilters
        '''
        from clonotypes.forms import ClonoFilterForm

        clonofilters = self.clonofilters_all()
        filter_forms = []
        for index, clonofilter in enumerate(clonofilters):
            filter_forms.append((clonofilter, ClonoFilterForm(initial=ClonoFilter.objects.filter(
                id=clonofilter.id).values()[0], prefix=str(index))))
        return filter_forms


    def filter_forms_list(self):
        '''
        Returns a list of filter forms for individual clonofilters
        '''
        from clonotypes.forms import ClonoFilterForm

        clonofilters = self.clonofilters_all()
        filter_forms = []
        for index, clonofilter in enumerate(clonofilters):
            filter_forms.append(ClonoFilterForm(initial=ClonoFilter.objects.filter(
                id=clonofilter.id).values()[0], prefix=str(index)))
        return filter_forms

    def colors_list(self):
        '''
        Returns a list of matplotlib color tuples in the ordered
        by the index of the clonofilter
        '''
        import pylab
        cm = pylab.get_cmap('gist_rainbow')
        clonofilters = sorted(self.clonofilters_all())
        returnable = [cm(1. * i / len(clonofilters))
                      for i in range(len(clonofilters))]
        return returnable

    def colors_dict(self):
        '''
        Returns a dict of colors indexed with clonofilters as keys and
        matplotlib colors and values
        '''
        import pylab

        returnable = {}
        clonofilters = sorted(self.clonofilters_all())
        cm = pylab.get_cmap('gist_rainbow')
        for index, clonofilter in enumerate(clonofilters):
            returnable[clonofilter] = cm(1. * index / len(clonofilters))
        return returnable

    def get_samples(self):
        '''
        Returns a queryset of samples associated with this comparsion
        '''
        samples = [
            clonofilter.sample for clonofilter in self.clonofilters_all()]
        return samples

    def get_amino_acids(self):
        ''' Returns the set of amino acids associated with the clonotypes
        retrieved from get_clonotypes()'''
        from clonotypes.models import AminoAcid
        clonotypes = self.get_clonotypes()
        return AminoAcid.objects.filter(id__in=clonotypes.values('recombination__amino_acid_id'))

    def get_recombinations(self):
        ''' Returns the set of recombinations associated with the clonotypes
        retrieved from get_clonotypes()'''
        from clonotypes.models import Recombination
        clonotypes = self.get_clonotypes()
        recombinations = Recombination.objects.filter(
            id__in=clonotypes.values('recombination_id'))
        return recombinations

    def get_clonotypes(self):
        '''
        Returns a union of the clonotypes for each member clonofilter queryset
        '''
        from clonotypes.models import Clonotype
        returnable = Clonotype.objects.none()
        for clonofilter in self.clonofilters_all():
            returnable |= clonofilter.get_clonotypes()

        return returnable

    def get_shared_amino_acids_old(self):
        ''' Returns a list of amino acids shared by the clonofilters
        defined in a comparison
        '''
        samples = self.get_samples()
        if len(samples) > 1:
            shared_amino_acid = reduce(lambda q, s: q.filter(recombination__clonotype__sample=s), samples, self.get_amino_acids())
            shared_amino_acid = shared_amino_acid.distinct()
            return shared_amino_acid
        else:
            return False

    def get_shared_amino_acids(self):
        ''' Returns a list of amino acids shared by the clonofilters
        defined in a comparison. Uses indexes to reduce joining time.
        '''
        from index.models import ClonoFilterToAmino
        from clonotypes.models import AminoAcid
        cfs = self.clonofilters_all()

        if len(cfs) > 1:
            cf2a_tuples = [ClonoFilterToAmino.objects.get_or_create(clonofilter=cf) for cf in cfs]
            amino_acids = [cf2a.amino_acids for cf2a, created in cf2a_tuples]
            shared_amino_acids_pks = set.intersection(*map(set, amino_acids))
            return AminoAcid.objects.filter(id__in=shared_amino_acids_pks)
        else:
            return False

    def get_shared_amino_acids_related(self):
        '''
        Returns the shared amino acids and related clonotypes
        as part of the _related_clonotypes field
        '''
        from clonotypes.models import AminoAcid, Recombination, Clonotype
        samples = self.get_samples()
        shared_amino_acids = self.get_shared_amino_acids()
        shared_queryset = AminoAcid.objects.filter(id__in=shared_amino_acids)
        amino_acid_dict = dict(
            [(amino_acid.id, amino_acid) for amino_acid in shared_queryset])

        clonotypes = Clonotype.objects.select_related().filter(recombination__amino_acid__in=shared_amino_acids).filter(sample__in=samples)
        clonotype_dict = {}

        for clonotype in clonotypes:
            clonotype_dict.setdefault(
                clonotype.recombination.amino_acid_id, []).append(clonotype)
        for id, related_clonotype in clonotype_dict.items():
            amino_acid_dict[id].related_clonotypes = related_clonotype

        return amino_acid_dict

    def get_shared_amino_acids_clonotypes(self):
        '''
        Given a comparison, returns the amino acids shared by all clonofilters within a comparison
        Returns a nested dict in the format:
            {'amino_acid': {'clonofilter': <sum_of_norm_counts>, 'clonofilter2': <sum of norm counts>}}
        '''
        from clonotypes.models import AminoAcid
        from collections import defaultdict
        from django.db.models import Q

        # Get a list of sample ids
        samples = self.get_samples()
        # Get all nucleotide_sequences belonging to samples and then only report those
        # that have at least len(samples) shared clonotypes
        returnable = defaultdict(lambda: defaultdict(lambda: .0))
        shared_amino_acid = self.get_shared_amino_acids()
        if shared_amino_acid:
            for amino_acid in shared_amino_acid:
                for recombination in amino_acid.recombination_set.all():
                    for clonotype in recombination.clonotype_set.all():
                        if clonotype.sample in samples:
                            returnable[
                                amino_acid][clonotype.sample] = clonotype
        return undefaulted(returnable)

    def get_shared_amino_acids_counts(self, **kwargs):
        '''
        Given a comparison, returns the amino acids shared by all clonofilters within a comparison
        By default returns the first 10 results, but can return different page
        or number of results by modifying kwargs
        Returns a nested dict in the format:
            {aa1_id: {'sequence': aa.sequence, 'clonofiters':{ cf_id1: float,
                              cf_id2: float,}}
        '''
        from clonotypes.models import AminoAcid
        from collections import defaultdict
        from django.db.models import Q

        # Get a list of clonofilters
        clonofilters = self.clonofilters_all()
        # Get a list of sample ids
        samples = self.get_samples()
        # Get a dict of sample id to clonofilter ids
        sampleid2cfid = defaultdict(lambda: [])
        for cf in clonofilters:
            sampleid2cfid[cf.sample.id].append(cf.id)
        # prefect clonofilters and index by their id
        cfid2cf = dict((cf.id, cf) for cf in clonofilters)

        # Set up the paginator
        try:
            paginator = Paginator(self.get_shared_amino_acids(), kwargs['per_page'])
        except:
            paginator = Paginator(self.get_shared_amino_acids(), 10)

        # Get the page number
        try:
            shared_amino_acids = paginator.page(kwargs['page'])
        except EmptyPage:
            shared_amino_acids = paginator.page(paginator.num_pages)
        except:
            shared_amino_acids = paginator.page(1)

        # Get all nucleotide_sequences belonging to samples and then only report those
        # that have at least len(samples) shared clonotypes
        returnable =  {}

        #for amino_acid in shared_amino_acids:
        for amino_acid in shared_amino_acids:
            amino_acid_dict = {}
            clonofilter_dict = defaultdict(lambda: 0)
            for recombination in amino_acid.recombination_set.all():
                for clonotype in recombination.clonotype_set.all():
                    if clonotype.sample in samples:
                        for cfid in sampleid2cfid[clonotype.sample.id]:
                            clonofilter_dict[cfid] += 1.0*clonotype.copy/cfid2cf[cfid].size()
            amino_acid_dict['clonofilters'] = undefaulted(clonofilter_dict)
            amino_acid_dict['sequence'] = amino_acid.sequence
            returnable[amino_acid.id] = amino_acid_dict

        return returnable, paginator.num_pages, paginator.count

    def get_shared_recombinations_counts(self):
        '''
        Given a comparison, returns the recombinations shared by all samples
        Returns a nested dict in the format:
            {'recombination.id': {'clonofilter': <sum_of_norm_counts>, 'clonofilter2': <sum of norm counts>}}
        '''
        from clonotypes.models import Recombination
        from collections import defaultdict

        # Get all nucleotide_sequences belonging to samples and then only report those
        # that have at least len(samples) shared clonotypes
        returnable = defaultdict(lambda: defaultdict(lambda: .0))

        # Get a list of clonofilters
        clonofilters = self.clonofilters_all()
        # Get a list of sample ids
        samples = self.get_samples()

        if len(samples) > 1:
            # Now get all clonotypes with these shared sequences
            shared_recombinations = reduce(lambda q, s: q.filter(
                clonotype__sample=s), samples, self.get_recombinations())
            shared_recombination = shared_recombinations.distinct()

            # Format the shared clonotypes as a dict of lists:
            # {'sequence': [<clonotype 1>, <clonotype2>]}
            for recombination in shared_recombinations:
                # Get the set of clonotypes for each recombination
                for clonotype in recombination.clonotype_set.all():
                    if clonotype.sample in samples:
                        returnable[recombination.nucleotide][
                            clonotype.sample] += clonotype.copy
                    # Get the set of samples for each clonotype
                    # Add # of reads per thing
#                returnable[recombination.nucleotide].append(clonotype)

        return undefaulted(returnable)

    def get_shared_clonotypes(self):
        '''
        Returns clonotypes that are shared by all members in the clonofilter
        '''
        from django.db.models import Count
        from clonotypes.models import Clonotype, Recombination
        from collections import defaultdict

        shared_clonotypes = [[]]
        # Get a list of sample ids
        samples = [
            clonofilter.sample for clonofilter in self.clonofilters_all()]
        # Get all nucleotide_sequences belonging to samples and then only report those
        # that have at least len(samples) shared clonotypes
        returnable = defaultdict(list)
        if len(samples) > 1:

            # Now get all clonotypes with these shared sequences
            #shared_recombinations = reduce(lambda q, s: q.filter(clonotype__sample=s), samples, Recombination.objects.all())
            shared_recombinations = reduce(lambda q, s: q.filter(
                clonotype__sample=s), samples, self.get_recombinations())
            shared_recombination = shared_recombinations.distinct()

            # Format the shared clonotypes as a dict of lists:
            # {'sequence': [<clonotype 1>, <clonotype2>]}
            for recombination in shared_recombinations:
                # Get the set of clonotypes for each recombination
                for clonotype in recombination.clonotype_set.all():
                    if clonotype.sample in samples:
                        returnable[recombination.nucleotide].append(clonotype)
                    # Get the set of samples for each clonotype
                    # Add # of reads per thing
#                returnable[recombination.nucleotide].append(clonotype)

        return dict(returnable)

    def get_shared_clonotypes_amino(self):
        '''
        Returns clonotypes that are shared by all members in the clonofilter
        '''
        from clonotypes.models import AminoAcid
        from collections import defaultdict
        from django.db.models import Q

        shared_clonotypes = [[]]
        # Get a list of sample ids
        samples = [
            clonofilter.sample for clonofilter in self.clonofilters_all()]
        # Get all nucleotide_sequences belonging to samples and then only report those
        # that have at least len(samples) shared clonotypes
        returnable = defaultdict(list)
        if len(samples) > 1:
            shared_amino_acid = reduce(lambda q, s: q.filter(recombination__clonotype__sample=s), samples, self.get_amino_acids())
            shared_amino_acid = shared_amino_acid.distinct()

            # Format the shared clonotypes as a dict of lists:
            # {'sequence': [<clonotype 1>, <clonotype2>]}
            for amino_acid in shared_amino_acid:
                for recombination in amino_acid.recombination_set.all():
                    for clonotype in recombination.clonotype_set.all():
                        if clonotype.sample in samples:
                            returnable[
                                amino_acid.sequence].append(clonotype.sample)

        return dict(returnable)

    def clonofilters_all(self):
        '''
        Converts the JSON-ified list of clonofilters into a list of
        ClonoFilter objects then returns the new list
        '''
        jsonDec = json.decoder.JSONDecoder()
        try:
            cfids = jsonDec.decode(self._clonofilters)
            if len(cfids):
                return [ClonoFilter.objects.get(id=cfid) for cfid in cfids]
        except:
            return []

    @staticmethod
    def default_from_samples(samples):
        '''
        In the case where samples are known, but no clonofilter has yet been defined,
        take in a list of samples, generate the default clonofilter, populate
        the Comparison object and save the object.
        '''
        # Get a list of default clonofilters for the samples
        default_clonofilters = [ClonoFilter.default_from_sample(sample)
                                for sample in samples]

        comparison, created = Comparison.get_or_create_from_clonofilters(
            default_clonofilters)

        return comparison

    @staticmethod
    def get_or_create_from_clonofilters(clonofilters):
        '''
        Given a list of clonofilters, checks to see if there is a comparison
        instance with exactly that list of clonofilters. If there is not one,
        create a new comparison instance with that exact list
        '''
        cfids = [cf.id for cf in clonofilters]
        if len(cfids):
            cfids.sort()
            comparison, created = Comparison.objects.get_or_create(_clonofilters=json.dumps(cfids))
            return comparison, created
        else:
            comparison, created = Comparison.objects.get_or_create(_clonofilters='[]')
            return comparison, created

    @staticmethod
    def get_or_create_from_clonofilters_defunct(clonofilters):
        '''
        Given a list of clonofilters, checks to see if there is a comparison
        instance with exactly that list of clonofilters. If there is not one,
        create a new comparison instance with that exact list
        '''
        from django.db.models import Count
        # Try to find a comparison with these particular clonofilters
        created = False
        try:
            # Works with sqlite3 but not with mysql
#            comparison = Comparison.objects.filter(clonofilters__in=clonofilters).annotate(num_filters=Count('clonofilters')).filter(num_filters=len(clonofilters)).exclude(id__in=Comparison.objects.annotate(all_filters=Count('clonofilters')).filter(all_filters__gt=len(clonofilters))).get()
            comparison = reduce(lambda q, cf: q.filter(clonofilters=cf), clonofilters, Comparison.objects.annotate(count=Count('clonofilters')))
            comparison = comparison.filter(count=len(clonofilters))[0]
        # If an existing clonofilter is not found, create
        # a new comparison given the default_clonofilters
#        except Comparison.DoesNotExist: # This exception was for the mysql
        except:
            comparison = Comparison()
            comparison.save()
            comparison.clonofilters.add(*clonofilters)
            comparison.save()
            created = True

        return comparison, created
        #return comparison

    def sample_names(self):
        '''
        Returns a dictionary of sample names indexed by clonofilter id
        '''
        return dict([(clonofilter.id,str(clonofilter.sample)) for clonofilter in self.clonofilters_all()])


class ComparisonColor(models.Model):
    ''' stores clonofilter colors for a comparison
    so they can be changed without generating a new clonofilter
    '''
    comparison = models.ForeignKey(Comparison)
    clonofilter = models.ForeignKey(ClonoFilter)
    color = models.CharField(max_length=9)
    #color = models.CharField(max_length=9, required=False)

    class Meta:
        unique_together = ("comparison", "clonofilter")

def hex_to_rgb(color):
    '''
    Given a hex color, return a list containing rgb ints in range [0,255]
    '''
    color = color.lstrip('#')
    cl = len(color)
    return [int(color[i:i+cl/3], 16) for i in range(0, cl, cl/3)]
