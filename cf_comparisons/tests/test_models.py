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

    def DONTtest_get_shared_amino_acids_counts_reports_a_sum_of_normalized_counts_as_nested_dict_value(self):
        '''todo: call on two datasets, one with norm factors, one without and make sure values are expected'''
        self.fail('todo: call on two datasets, one with norm factors, one without and make sure values are expected')

    def DONTtest_get_shared_recombinations_counts_reports_a_sum_of_normalized_counts_as_nested_dict_value(self):
        '''todo: call on two datasets, one with norm factors, one without and make sure values are expected'''
        self.fail('todo: call on two datasets, one with norm factors, one without and make sure values are expected')

    def test_get_shared_amino_acids_returns_a_list_of_shared_amino_acids(self):
        samples = [clonofilter.sample for clonofilter in self.comparison.clonofilters.all()]
        shared_amino_acid = reduce(lambda q, s: q.filter(recombination__clonotype__sample=s), samples, self.comparison.get_amino_acids())
        self.assertEqual(set(shared_amino_acid), set(self.comparison.get_shared_amino_acids()))

    def test_get_shared_amino_acids_counts_returns_a_nested_dict_of_floats(self):
        shared_amino_acids = self.comparison.get_shared_amino_acids_counts()
        self.assertIsInstance(shared_amino_acids, dict)

        for nested in shared_amino_acids.values():
            self.assertIsInstance(nested, dict)
            for count_sum in nested.values():
                self.assertIsInstance(count_sum, float)

    def test_get_shared_recombinations_counts_returns_a_nested_dict_of_floats(self):
        '''
        Tests that the method get_shared_clonotypes() returns a list of lists of clonotypes.
        Each item in the outer list is a shared clonotype and each item in the inner
        list is a sample-specific clonotype
        '''
        shared_recombinations = self.comparison.get_shared_recombinations_counts()
        self.assertIsInstance(shared_recombinations, dict)

        for nested in shared_recombinations.values():
            self.assertIsInstance(nested, dict)
            for count_sum in nested.values():
                self.assertIsInstance(count_sum, float)

    def test_get_amino_acids_returns_a_union_of_individual_clonofilter_querysets(self):
        from clonotypes.models import AminoAcid
        from test_utils.factories import AminoAcidFactory
        amino_acids = AminoAcid.objects.all()
        self.assertEqual(map(repr, amino_acids),
                         map(repr, self.comparison.get_amino_acids()))
        # Make sure nonmember amino acids are not included
        AminoAcidFactory()
        self.assertNotEqual(map(repr, AminoAcid.objects.all()),
                            map(repr, self.comparison.get_amino_acids()))

    def test_get_recombinations_returns_a_union_of_individual_clonofilter_querysets(self):
        from clonotypes.models import Recombination
        from test_utils.factories import RecombinationFactory, ClonotypeFactory
        recombinations = Recombination.objects.all()
        self.assertEqual(map(repr, recombinations),
                         map(repr, self.comparison.get_recombinations()))

        # Make sure nonmember recombinations are not included
        nonmember_recombination = RecombinationFactory()
        ClonotypeFactory(recombination=nonmember_recombination)
        self.assertNotEqual(map(repr, Recombination.objects.all()),
                            map(repr, self.comparison.get_recombinations()))

    def test_get_clonotypes_returns_a_union_of_individual_clonofilter_querysets(self):
        from test_utils.factories import SampleFactory, ClonotypeFactory
        from clonotypes.models import Clonotype

        cfs = self.comparison.clonofilters.all()
        qs_union = cfs[0].get_clonotypes() | cfs[1].get_clonotypes()
        self.assertEqual(map(repr, qs_union),
                         map(repr, self.comparison.get_clonotypes()))

        # Make sure that nonmember clonotypes are not included
        nonmember_sample = SampleFactory()
        nonmember_clonotype = ClonotypeFactory(sample=nonmember_sample)
        self.assertNotEqual(map(repr, Clonotype.objects.all()),
                            map(repr, self.comparison.get_clonotypes()))

    def test_nonempty_shared_clonotype_amino_set_returns_clonotypes(self):
        shared_clonotypes = self.comparison.get_shared_clonotypes_amino()
        s1 = Sample.objects.all()[0]
        s2 = Sample.objects.all()[1]
        self.assertEqual({u'CASSLGPLAEKETQYF': [s1, s2]
                          }, shared_clonotypes)
    def test_get_or_create_from_clonofilters_returns_one_comparison_if_two_supersets_exist(self):
        '''
        This test replicates a bug where multiple comparisons are returned if
        multiple comparisons exist which contain a subset of clonofilters. This
        is most evident when creating a new comparison from a list of samples
        '''
        s1 = Sample.objects.all()[0]
        s2 = Sample.objects.all()[1]
        Comparison.default_from_samples([s1])
        Comparison.default_from_samples([s1,s2])
        Comparison.default_from_samples([s1])

        self.assertEqual(2, Comparison.objects.all().count())

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
