from django.test import TestCase
from cf_comparisons.models import Comparison, ComparisonColor
from clonotypes.models import ClonoFilter
from test_utils.ghetto_factory import make_fake_patient_with_3_clonotypes, make_fake_comparison_with_2_samples
from samples.models import Sample


class ComparsionModelMethodsTest(TestCase):
    '''
    Used to test comparison methods.
    '''
    def setUp(self):
        make_fake_comparison_with_2_samples()
        self.comparison = Comparison.objects.get()

    def DONTtest_get_shared_recombinations_counts_reports_a_sum_of_normalized_counts_as_nested_dict_value(self):
        '''todo: call on two datasets, one with norm factors, one without and make sure values are expected'''
        self.fail('todo: call on two datasets, one with norm factors, one without and make sure values are expected')

    def test_comparison_sample_names_returns_dictionary_of_sample_names_indexed_by_cfid(self):
        self.assertEqual({1: 'test patient 2012-12-12 cd4+', 2: 'test patient 2012-12-13 cd4+'} , self.comparison.sample_names())

    def test_add_samples_add_samples_to_comparison(self):
        from test_utils.factories import SampleFactory
        sample = SampleFactory()
        comp = self.comparison.add_samples([sample])
        self.assertEqual(len(Comparison.objects.all()), 2)
        self.assertTrue(sample in set([cf.sample for cf in comp.clonofilters.all()]))

    def test_update_comparison_preserves_colors(self):
        from django.forms import model_to_dict
        comp = Comparison.objects.get()
        cfs = ClonoFilter.objects.all()
        cfd0 = model_to_dict(cfs[0])
        cfd1 = model_to_dict(cfs[1])
        old_colors = comp.colors()
        comp.set_colors({cfd0['id']: "#000000"})
        self.assertNotEqual(old_colors, comp.colors())

        new_cfd0 = {'min_copy': 1}
        new_cfd1 = {'min_length': 1}
        new_comp = comp.update({cfd0['id']: new_cfd0,
                                cfd1['id']: new_cfd1})

        self.assertEqual(set(comp.colors().values()),
                set(new_comp.colors().values()))

    def test_update_comparison_given_a_set_of_update_dicts(self):
        from django.forms import model_to_dict
        comp = Comparison.objects.get()
        cfs = ClonoFilter.objects.all()
        cfd0 = model_to_dict(cfs[0])
        cfd1 = model_to_dict(cfs[1])

        new_cfd0 = {'min_copy': 1}
        new_cfd1 = {'min_length': 1}

        new_comp = comp.update({cfd0['id']: new_cfd0,
                                cfd1['id']: new_cfd1})
#        new_comp = comp.update([{'key': cfd0['id'],
#                                'values': new_cfd0},
#                                {'key':cfd1['id'],
#                                 'values': new_cfd1}])
        self.assertEqual(len(Comparison.objects.all()), 2)
        self.assertNotEqual(comp.id, new_comp.id)

    def test_get_samples_returns_list_of_samples_only_in_comparison(self):
        samples = Sample.objects.all()
        self.assertEqual(map(repr, samples),
                         map(repr, self.comparison.get_samples()))

    def test_colors_list_returns_a_list_of_colors(self):
        self.assertEqual(
            [(1.0, 0.0, 0.16, 1.0), (0.0, 1.0, 0.54817625975121254, 1.0)],
            self.comparison.colors_list())

    def test_colors_dict_returns_a_dict_of_colors(self):
        self.assertEqual(
            [(0.0, 1.0, 0.54817625975121254, 1.0), (1.0, 0.0,
                                                    0.16, 1.0)].sort(),
            self.comparison.colors_dict().values().sort())
        self.assertIsInstance(
            self.comparison.colors_dict().keys()[0], ClonoFilter)

    def test_get_shared_amino_acids_returns_a_list_of_shared_amino_acids(self):
        samples = [clonofilter.sample for clonofilter in self.comparison.clonofilters.all()]
        shared_amino_acid = reduce(lambda q, s: q.filter(recombination__clonotype__sample=s), samples, self.comparison.get_amino_acids())
        self.assertEqual(set(
            shared_amino_acid), set(self.comparison.get_shared_amino_acids()))

    def test_get_shared_amino_acids_clonotypes_returns_a_nested_dict_of_clonotypes(self):
        from clonotypes.models import Clonotype
        shared_amino_acids = self.comparison.get_shared_amino_acids_clonotypes(
        )
        self.assertIsInstance(shared_amino_acids, dict)

        for nested in shared_amino_acids.values():
            self.assertIsInstance(nested, dict)
            for clonotype in nested.values():
                self.assertIsInstance(clonotype, Clonotype)

    def test_get_shared_amino_acids_counts_returns_a_d3_compatible_dict_of_amino_acid_counts(self):
        '''
        Tests that get_shared_amino_acids_counts returns a dict in the format
            {aa1_id: {'sequence': aa.sequence, 'clonofiters':{ cf_id1: float,
                              cf_id2: float,}}
        '''
        from clonotypes.models import AminoAcid, ClonoFilter

        shared_amino_acids = self.comparison.get_shared_amino_acids_counts()
        self.assertIsInstance(shared_amino_acids, dict)
        self.assertNotEqual(shared_amino_acids, {})
        for aa_id, values in shared_amino_acids.iteritems():
            self.assertIsInstance(values['sequence'], unicode)
            for cf_id, value in values['clonofilters'].iteritems():
                self.assertTrue(ClonoFilter.objects.get(id=cf_id))
                self.assertIsInstance(value, float)

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
        Comparison.default_from_samples([s1, s2])
        Comparison.default_from_samples([s1])

        self.assertEqual(2, Comparison.objects.all().count())

    def test_get_shared_clonotypes_returns_empty_dict_if_only_one_clonofilter_is_provided(self):
        cf = ClonoFilter.objects.all()[0]
        comparison, created = Comparison.get_or_create_from_clonofilters([cf])
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

    def test_get_shared_amino_acids_related_returns_queryset_of_recombinations_and_clonotypes(self):
        ''' Returns a queryset of shared amino acids between two samples
        along with related recombination and clonotype fields
        '''
        shared_amino_acids = self.comparison.get_shared_amino_acids_related()
        shared_amino_acid = shared_amino_acids[1]
#        recombination = shared_amino_acid.recombination_set.all().get()
#        self.assertEqual(recombination, shared_amino_acid._related_recombination[0])

        clonotypes = self.comparison.get_shared_clonotypes()
        self.assertEqual(clonotypes.values().sort(), shared_amino_acid.related_clonotypes.sort())

    def test_get_shared_amino_acids_related_returns_only_clonotypes_belonging_to_shared_clonofilters(self):
        from test_utils.factories import SampleFactory, ClonotypeFactory
        from clonotypes.models import AminoAcid
        s3 = SampleFactory()
        aa = AminoAcid.objects.all()[0]
        r = aa.recombination_set.all()[0]

        c = ClonotypeFactory(
                sample=s3,
                recombination = r)

        for shared_amino_acid in self.comparison.get_shared_amino_acids_related().values():
            for clonotype in shared_amino_acid.related_clonotypes:
                self.assertNotEqual(c, clonotype)

    def DONTtest_shared_amino_acid_sums_returns_double_dict_indexed_by_amino_acid_and_sample(self):
        amino_acids_sums = self.comparison.shared_amino_counts()
        samples = Sample.objects.all()
        shared_amino_acids = self.comparison.get_shared_amino_acids_related()
        self.fail('todo')

    def test_filter_forms_dict_returns_a_dict_of_filter_forms_indexed_by_clonofilter_given_a_comparison_id(self):
        from clonotypes.forms import ClonoFilterForm
        comparison = Comparison.objects.get()
        filter_forms = comparison.filter_forms_dict()
        for filter_form in filter_forms.values():
            self.assertIsInstance(filter_form, ClonoFilterForm)

    def test_filter_forms_list_returns_a_list_of_filter_forms_given_a_comparison_id(self):
        from clonotypes.forms import ClonoFilterForm
        comparison = Comparison.objects.get()
        filter_forms = comparison.filter_forms_list()
        for filter_form in filter_forms:
            self.assertIsInstance(filter_form, ClonoFilterForm)


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



class ComparisonColorModelTest(TestCase):
    '''
    Tests colors
    '''

    def setUp(self):
        make_fake_comparison_with_2_samples()
        self.s = Sample.objects.all()[0]
        self.cf = list(ClonoFilter.objects.all())
        self.comp = Comparison.objects.get()

    def test_rgba_colors_returns_dict_of_rgba_values(self):
        import re
        color_dict = self.comp.rgba_colors()
        for cf_id, color in color_dict.iteritems():
            p = re.compile('rgba\( *\d+ *, *\d+ *, *\d+ *, *\d+ *\\)')
            self.assertTrue(p.match(color_dict[cf_id]))


    def test_colors_automagically_assigns_colors_if_they_dont_exist(self):
        color_dict = self.comp.colors()
        cfs = self.comp.clonofilters.all()
        for cf in cfs:
            self.assertNotEqual(color_dict[cf.id], None)

    def test_colors_object_stores_clonofilter_colors(self):
        # given a comparison you can add a color for a specific clonofilter in that
        # comparison
        color = "#000000"
        color_dict = dict(zip([self.cf[0].id], [color]))
        self.comp.set_colors(color_dict)
        self.assertEqual(self.comp.colors()[self.cf[0].id], color)

    def test_given_a_comparison_and_a_clonofilter_you_can_set_a_color(self):
        cf1 = self.cf[0]
        cc = ComparisonColor(comparison=self.comp, clonofilter=cf1, color="#000000")
        cc.save()
        comp_color = ComparisonColor.objects.get()
        self.assertEqual(comp_color.color, "#000000")
