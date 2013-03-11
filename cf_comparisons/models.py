from django.db import models
from clonotypes.models import ClonoFilter


class Comparison(models.Model):
    clonofilters = models.ManyToManyField(ClonoFilter)

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
