from django.db import models
from clonotypes.models import ClonoFilter
from utils.utils import undefaulted


class Comparison(models.Model):
    clonofilters = models.ManyToManyField(ClonoFilter)

    def colors_list(self):
        '''
        Returns a list of matplotlib color tuples in the ordered
        by the index of the clonofilter
        '''
        import pylab
        cm = pylab.get_cmap('gist_rainbow')
        clonofilters = sorted(self.clonofilters.all())
        returnable = [cm(1.*i/len(clonofilters)) for i in range(len(clonofilters))]
        return returnable

    def colors_dict(self):
        '''
        Returns a dict of colors indexed with clonofilters as keys and
        matplotlib colors and values
        '''
        import pylab

        returnable = {}
        clonofilters = sorted(self.clonofilters.all())
        cm = pylab.get_cmap('gist_rainbow')
        for index, clonofilter in enumerate(clonofilters):
            returnable[clonofilter] = cm(1.*index/len(clonofilters))
        return returnable

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
        recombinations = Recombination.objects.filter(id__in=clonotypes.values('recombination_id'))
        return recombinations

    def get_clonotypes(self):
        '''
        Returns a union of the clonotypes for each member clonofilter queryset
        '''
        from clonotypes.models import Clonotype
        returnable = Clonotype.objects.none()
        for clonofilter in self.clonofilters.all():
            returnable |= clonofilter.get_clonotypes()

        return returnable

    def get_shared_amino_acids(self):
        ''' Returns a list of amino acids shared by the clonofilters
        defined in a comparison
        '''
        samples = [clonofilter.sample for clonofilter in self.clonofilters.all()]
        if len(samples) > 1:
            shared_amino_acid = reduce(lambda q, s: q.filter(recombination__clonotype__sample=s), samples, self.get_amino_acids())
            shared_amino_acid = shared_amino_acid.distinct()
            return shared_amino_acid
        else:
            return False

    def get_shared_amino_acids_counts(self):
        '''
        Given a comparison, returns the amino acids shared by all clonofilters within a comparison
        Returns a nested dict in the format:
            {'amino_acid': {'clonofilter': <sum_of_norm_counts>, 'clonofilter2': <sum of norm counts>}}
        '''
        from clonotypes.models import AminoAcid
        from collections import defaultdict
        from django.db.models import Q

        # Get a list of sample ids
        samples = [clonofilter.sample for clonofilter in self.clonofilters.all()]
        # Get all nucleotide_sequences belonging to samples and then only report those
        # that have at least len(samples) shared clonotypes
        returnable = defaultdict(lambda: defaultdict(lambda: .0))
        shared_amino_acid = self.get_shared_amino_acids()
        if shared_amino_acid:

            # Format the shared clonotypes as a dict of lists:
            # {'sequence': [<clonotype 1>, <clonotype2>]}
            for amino_acid in shared_amino_acid:
                for recombination in amino_acid.recombination_set.all():
                    for clonotype in recombination.clonotype_set.all():
                        if clonotype.sample in samples:
                            returnable[amino_acid][clonotype.sample] += clonotype.copy
                            #returnable[amino_acid.sequence][clonotype.sample] += clonotype.copy

        return undefaulted(returnable)

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
        clonofilters = self.clonofilters.all()
        # Get a list of sample ids
        samples = [clonofilter.sample for clonofilter in clonofilters]

        if len(samples) > 1:

            # Now get all clonotypes with these shared sequences
            shared_recombinations = reduce(lambda q, s: q.filter(clonotype__sample=s), samples, self.get_recombinations())
            shared_recombination = shared_recombinations.distinct()

            # Format the shared clonotypes as a dict of lists:
            # {'sequence': [<clonotype 1>, <clonotype2>]}
            for recombination in shared_recombinations:
                # Get the set of clonotypes for each recombination
                for clonotype in recombination.clonotype_set.all():
                    if clonotype.sample in samples:
                        returnable[recombination.nucleotide][clonotype.sample] += clonotype.copy
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
        samples = [clonofilter.sample for clonofilter in self.clonofilters.all()]
        # Get all nucleotide_sequences belonging to samples and then only report those
        # that have at least len(samples) shared clonotypes
        returnable = defaultdict(list)
        if len(samples) > 1:

            # Now get all clonotypes with these shared sequences
            #shared_recombinations = reduce(lambda q, s: q.filter(clonotype__sample=s), samples, Recombination.objects.all())
            shared_recombinations = reduce(lambda q, s: q.filter(clonotype__sample=s), samples, self.get_recombinations())
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
        samples = [clonofilter.sample for clonofilter in self.clonofilters.all()]
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
                            returnable[amino_acid.sequence].append(clonotype.sample)

        return dict(returnable)

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

        comparison = Comparison.get_or_create_from_clonofilters(default_clonofilters)

        return comparison

    @staticmethod
    def get_or_create_from_clonofilters(clonofilters):
        '''
        Given a list of clonofilters, checks to see if there is a comparison
        instance with exactly that list of clonofilters. If there is not one,
        create a new comparison instance with that exact list
        '''
        from django.db.models import Count
        # Try to find a comparison with these particular clonofilters
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

        return comparison
