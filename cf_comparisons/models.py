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
        from django.db.models import Count

        # Get a list of default clonofilters for the samples
        default_clonofilters = [ClonoFilter.default_from_sample(
            sample) for sample in samples]

        # Try to find a comparison with these particular clonofilters
        try:
            comparison  = Comparison.objects.filter(clonofilters__in=samples).annotate(num_filters=Count('clonofilters')).filter(num_filters=len(samples)).exclude(id__in=Comparison.objects.annotate(all_filters=Count('clonofilters')).filter(all_filters__gt=len(samples))).get()
        # If an existing clonofilter is not found, create
        # a new comparison given the default_clonofilters
        except Comparison.DoesNotExist:
            comparison = Comparison()
            comparison.save()
            comparison.clonofilters.add(*default_clonofilters)
            comparison.save()

        return comparison
