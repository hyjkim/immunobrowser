from django.db import models
from clonotypes.models import ClonoFilter


class Comparison(models.Model):
    clonofilters = models.ManyToManyField(ClonoFilter)

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
            shared_recombinations = reduce(lambda q, s: q.filter(clonotype__sample=s), samples, Recombination.objects.all())
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
            shared_amino_acid = reduce(lambda q, s: q.filter(recombination__clonotype__sample=s), samples, AminoAcid.objects.all())
            #shared_amino_acid = reduce(lambda q, s: q.filter(samples=s), samples, AminoAcid.objects.all())
            shared_amino_acid = shared_amino_acid.distinct()

            # Format the shared clonotypes as a dict of lists:
            # {'sequence': [<clonotype 1>, <clonotype2>]}
            for amino_acid in shared_amino_acid:
                for recombination in amino_acid.recombination_set.all():
                    for clonotype in recombination.clonotype_set.all():
                        if clonotype.sample in samples:
                            returnable[amino_acid.sequence].append(clonotype.sample)

#                for sample in amino_acid.samples.all():
#                    returnable[amino_acid.sequence].append(sample)
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
            comparison = Comparison.objects.filter(clonofilters__in=clonofilters).annotate(num_filters=Count('clonofilters')).filter(num_filters=len(clonofilters)).exclude(id__in=Comparison.objects.annotate(all_filters=Count('clonofilters')).filter(all_filters__gt=len(clonofilters))).get()
        # If an existing clonofilter is not found, create
        # a new comparison given the default_clonofilters
        except Comparison.DoesNotExist:
            comparison = Comparison()
            comparison.save()
            comparison.clonofilters.add(*clonofilters)
            comparison.save()

        return comparison
