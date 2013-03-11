from django.test import TestCase
from cf_comparisons.models import Comparison
from clonotypes.models import ClonoFilter
#from mock import patch
from test_utils.ghetto_factory import make_fake_patient_with_3_clonotypes
from samples.models import Sample


class ComparisonModelTest(TestCase):
    def setUp(self):
        make_fake_patient_with_3_clonotypes()
        self.s = Sample.objects.get()

    def test_get_or_create_from_clonofilters_does_not_create_a_new_comparison_if_one_already_exists_for_the_set_of_clonofilters(self):
        cf_1 = ClonoFilter(sample=self.s)
        cf_1.save()

        cf_2 = ClonoFilter(sample=self.s)
        cf_2.save()

        Comparison.get_or_create_from_clonofilters([cf_1, cf_2])
        Comparison.get_or_create_from_clonofilters([cf_1, cf_2])

        self.assertEqual(1, Comparison.objects.all().count())

    def test_default_with_samples_does_not_create_a_new_Comparison_if_one_already_exists_for_those_samples(self):
        '''
        Should check for a Comparison with the samples prior to creating a new one
        '''
        samples = [self.s]

        comp_1 = Comparison.default_from_samples(samples)
        comp_2 = Comparison.default_from_samples(samples)

        self.assertEqual(1, Comparison.objects.all().count())

    def test_default_with_samples_populates_a_comparison_object_with_default_clonofilters(self):
        '''
        We should be able to create a Comparison instance given just a list of samples.
        The ClonoFilters in the Comparison object should be the default ClonoFilter of
        each sample.
        '''
        samples = [self.s]

        comp = Comparison.default_from_samples(samples)

        cf = ClonoFilter.objects.get()

        self.assertEqual(set([cf]), set(comp.clonofilters.all()))

    def test_comparison_stores_many_clonofilters(self):
        """
        Test that a comparison object can story many clonofilters
        """

        cf_1 = ClonoFilter(sample=self.s)
        cf_1.save()

        cf_2 = ClonoFilter(sample=self.s)
        cf_2.save()

        comp = Comparison()
        comp.save()

        comp.clonofilters.add(cf_1)
        comp.clonofilters.add(cf_2)

        self.assertEqual(set([cf_1, cf_2]), set(comp.clonofilters.all()))
