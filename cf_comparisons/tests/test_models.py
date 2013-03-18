from django.test import TestCase
from cf_comparisons.models import Comparison
from clonotypes.models import ClonoFilter
#from mock import patch
from test_utils.ghetto_factory import make_fake_patient_with_3_clonotypes, make_fake_comparison_with_2_samples
from samples.models import Sample

class ComparsionModelMethodsTest(TestCase):
    '''
    Used to test comparison methods.
    '''
    def setUp(self):
        make_fake_comparison_with_2_samples()
        self.comparison = Comparison.objects.get()

    def test_get_shared_clonotypes_returns_empty_dict_if_only_one_clonofilter_is_provided(self):
        cf = ClonoFilter.objects.all()[0]
        comparison = Comparison.get_or_create_from_clonofilters([cf])
        self.assertEqual({}, comparison.get_shared_clonotypes())

    def test_nonempty_shared_clonotype_set_returns_clonotypes(self):
        from clonotypes.models import Clonotype
        shared_clonotypes = self.comparison.get_shared_clonotypes()
        self.assertIsInstance(shared_clonotypes['GGACTCGGCCATGTATCTCTGTGCCAGCAGCTTAGGTCCCCTAGCTGAAAAAGAGACCCA'][0], Clonotype)

    def test_get_shared_clonotypes_returns_a_dict(self):
        '''
        Tests that the method get_shared_clonotypes() returns a list of lists of clonotypes.
        Each item in the outer list is a shared clonotype and each item in the inner
        list is a sample-specific clonotype
        '''
        shared_clonotypes = self.comparison.get_shared_clonotypes()
        #self.assertEqual('', shared_clonotypes)
        self.assertIsInstance(shared_clonotypes, dict)


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
