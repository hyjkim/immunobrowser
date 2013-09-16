from django.test import TestCase
from patients.models import Patient
from samples.models import Sample
from clonotypes.models import Clonotype, AminoAcid, Recombination, ClonoFilter, ClonoFilter2
from test_utils.ghetto_factory import make_fake_patient, make_fake_patient_with_3_clonotypes
import re
from test_utils.factories import AminoAcidFactory, SampleFactory, ClonotypeFactory, RecombinationFactory


class ClonotypeTest(TestCase):
    def test_clonotype_belonging_to_a_private_sample_is_not_viewable(self):
        self.fail('todo')

    def test_clonotypes_have_these_required_fields(self):
        s = SampleFactory()
        r = RecombinationFactory()
        data = {'sample': s,
                'sequence_id': 'test',
                'container': 'test',
                'normalized_frequency': 0.1,
                'normalized_copy': 1,
                'copy': 1,
                'raw_frequency': 0.1,
                'recombination': r,
                }
        c = Clonotype()
        for key, value in data.items():
            setattr(c, key, value)
        c.save()

        c_in_db = Clonotype.objects.get()

        for key, value in data.items():
            self.assertEqual(
                value, getattr(c_in_db, key), 'key value %s not equal' % key)


class RecombinationModelTest(TestCase):

    def test_recombination_belonging_to_only_to_a_private_clonotype_is_not_viewable(self):
        self.fail('todo')

    def test_recombinations_have_an_optional_amino_acid(self):
        aa = AminoAcidFactory()
        r = RecombinationFactory()
        r.amino_acid = aa
        r.save()
        self.assertEqual(aa, r.amino_acid)

    def test_recombinations_have_these_required_fields(self):
        data = {
            'nucleotide': 'ATGCATGC',
            'v_family_name': 'v1',
            'v_gene_name': '1',
            'v_ties': '1,2',
            'd_gene_name': '2',
            'j_gene_name': 'j3',
            'j_ties': 'j4,j5',
            'v_deletion': 2,
            'd5_deletion': 3,
            'd3_deletion': 2,
            'j_deletion': 3,
            'n2_insertion': 4,
            'n1_insertion': 5,
            'v_index': 3,
            'n1_index': 4,
            'n2_index': -1,
            'd_index': 10,
            'j_index': 5,
            'sequence_status': 'Productive',
            'cdr3_length': 42,
        }
        r = Recombination()
        for key, value in data.items():
            setattr(r, key, value)
        r.save()

        r_in_db = Recombination.objects.get()

        for key, value in data.items():
            self.assertEqual(
                value, getattr(r_in_db, key), 'key value %s not equal' % key)

    def test_functionality_states_returns_list_of_all_functionality_states_in_db(self):
        make_fake_patient_with_3_clonotypes()
        self.assertIsInstance(Recombination.functionality_states(), list)
        self.assertEqual([u'Productive', u'Out of frame'],
                         Recombination.functionality_states())

    def test_v_family_names_returns_list_of_distinct_v_family_names(self):
        make_fake_patient_with_3_clonotypes()
        self.assertIsInstance(Recombination.v_family_names(), list)
        self.assertEqual(['7', '8', '9'], Recombination.v_family_names())

    def test_j_gene_names_returns_list_of_distinct_j_gene_names(self):
        make_fake_patient_with_3_clonotypes()
        self.assertIsInstance(Recombination.j_gene_names(), list)
        self.assertEqual(
            [u'TRBJ2-5', u'TRBJ2-4'], Recombination.j_gene_names())

    def test_parse_nucleotide_should_not_create_a_span_if_index_is_lt_0(self):
        ''' Adaptive uses -1 in the index field to represent the lack of
        that element. This test makes sure rendered text does no create a span
        for an empty region '''
        make_fake_patient()
        r = Recombination.objects.get()
        r.n1_index = -1
        pr = r.parsed_nucleotide()

        self.assertNotIn('<span class="n1_additions"', pr)

        r = Recombination.objects.get()
        r.d_index = -1
        pr = r.parsed_nucleotide()

        self.assertNotIn('<span class="d_gene"', pr)

        r = Recombination.objects.get()
        r.n2_index = -1
        pr = r.parsed_nucleotide()

        self.assertNotIn('<span class="n2_additions"', pr)

    def test_parsed_nucleotide_should_wrap_spans_around_nucleotide_groups(self):
        make_fake_patient()
        r = Recombination.objects.get()
        pr = r.parsed_nucleotide()

        # Test v
        regex = re.compile('.*<span class="v_gene">(.*?)</span>')
        match = regex.match(pr)
        self.assertEqual(len(match.groups()[0]), r.n2_index)

        # N2
        regex = re.compile('.*<span class="n2_additions">(.*?)</span>')
        match = regex.match(pr)
        num_n2_additions = r.d_index - r.n2_index
        self.assertEqual(len(match.groups()[0]), num_n2_additions)

        # D
        regex = re.compile('.*<span class="d_gene">(.*?)</span>')
        match = regex.match(pr)
        d_length = r.n1_index - r.d_index
        self.assertEqual(len(match.groups()[0]), d_length)

        # N1
        regex = re.compile('.*<span class="n1_additions">(.*?)</span>')
        match = regex.match(pr)
        num_n1_additions = r.j_index - r.n1_index
        self.assertEqual(len(match.groups()[0]), num_n1_additions)

        # J
        regex = re.compile('.*<span class="j_gene">(.*?)</span>')
        match = regex.match(pr)
        j_length = len(r.nucleotide) - r.j_index
        self.assertEqual(len(match.groups()[-1]), j_length)

    def test_parsed_nucleotide_should_return_nucleotide_sequence(self):
        make_fake_patient()
        r = Recombination.objects.get()
        pr = r.parsed_nucleotide()
        no_html = re.sub('<[^<]+?>', '', pr)
        self.assertEqual(r.nucleotide, no_html)

    def test_parsed_nucleotide_returns_a_string(self):
        make_fake_patient()
        r = Recombination.objects.get()
        pr = r.parsed_nucleotide()
        self.assertIsInstance(pr, str)



class AminoAcidModelTest(TestCase):

    def test_amino_acid_search_converts_lower_case_terms_to_uppercase(self):
        AminoAcidFactory(sequence="CASSS")
        self.assertEqual(1, len(AminoAcid.objects.search(['cAS'])))

    def test_amino_acid_belonging_to_only_to_a_private_recombination_is_not_viewable(self):
        self.fail('todo')

    def test_amino_acid_should_have_amino_acid_sequence(self):
        data = {'sequence': 'CASS'}
        aa = AminoAcid()

        for key, value in data.items():
            setattr(aa, key, value)
        aa.save()
        aa_in_db = AminoAcid.objects.get()
        for key, value in data.items():
            self.assertEqual(value, getattr(aa_in_db, key))

    def test_amino_acid_can_be_made_from_multiple_recombinations(self):
        aa = AminoAcidFactory()
        r = RecombinationFactory()
        r.amino_acid = aa
        r.save()
        r2 = RecombinationFactory()
        r2.amino_acid = aa
        r2.save()
        self.assertEqual(r, aa.recombination_set.all()[0])
        self.assertEqual(r2, aa.recombination_set.all()[1])

    def DONTtest_amino_acid_can_exist_in_multiple_samples(self):
        '''
        Because there's no intrinsic link between samples and
        amino acid sequences, we store all the samples that contain
        this amino acid sequence here. This should make querying for
        shared amino acids much faster.
        '''
        s = SampleFactory()
        s2 = SampleFactory()
        aa = AminoAcidFactory()
        aa.samples.add(s)
        aa.samples.add(s2)
        self.assertEqual(set([s, s2]), set(aa.samples.all()))


class ClonotypeModelTest(TestCase):
    def test_clonotypes_have_an_optional_amino_acid(self):
        aa = AminoAcidFactory()
        c = ClonotypeFactory()
        c.amino_acid = aa
        c.save()
        self.assertEqual(aa, c.amino_acid)

    def DONT_test_bulk_insert_of_tsv_to_database(self):
        # Make a test sample
        p = Patient()
        p.save()
        s = Sample(patient=p)
        s.save()

       # Model can read in a file
        Clonotype.import_tsv(s, 'clonotypes/tests/data/test_adaptive.tsv')
        all_clonotypes = Clonotype.objects.all()
        self.assertEquals(len(all_clonotypes), 100)

    def test_bulk_insert_should_throw_error_if_file_does_not_exist(self):
        p = Patient()
        p.save()
        s = Sample(patient=p)
        s.save()
        self.assertRaises(
            IOError, Clonotype.import_tsv, s, '/fake/path/to/fake/file')

    def test_create_clonotypes_for_a_sample(self):
        p = Patient()
        p.save()
        s = Sample(patient=p)
        s.save()
        r = RecombinationFactory()

        c = Clonotype(
            sample=s,
            recombination=r,
            sequence_id='C0FW0ACXX_1_Patient-15-D_1',
            container='UCSC-Kim-P01-01',
            normalized_frequency=9.336458E-6,
            normalized_copy=2,
            raw_frequency=1.6548345E-5,
            copy=2,
        )
        c.save()

        # Get all clonotypes from database
        all_clonotypes = Clonotype.objects.all()

        self.assertEqual(all_clonotypes[0], c)


class ClonoFilterModelTest(TestCase):
    def setUp(self):
        make_fake_patient_with_3_clonotypes()
        self.s = Sample.objects.get()
        self.f = ClonoFilter(sample=self.s)
        self.f.save()

    def test_min_copy_defaults_to_min_copy_for_that_sample(self):
        from django.db.models import Min
        aggregate = Clonotype.objects.aggregate(Min('copy'))
        min_copy = aggregate['copy__min']
        self.assertEqual(self.f.min_copy, min_copy)
        self.fail('todo')

    def test_css_class_returns_clonofilter_class_string(self):
        self.assertEqual(self.f.css_class(), "cf-1")

    def test_update_generates_a_new_clonofilter_and_merges_filters_with_existing(self):
        from django.forms.models import model_to_dict
        self.f.min_copy = 1
        self.f.save()
        new_cf, new_created = self.f.update({'max_length': 50})
        test_cf, test_created = ClonoFilter.objects.get_or_create(**{
            'sample': self.s,
            'min_copy': 1,
            'max_length': 50
        })

        self.assertEqual(new_created, True)
        self.assertEqual(test_created, False)
        self.assertEqual(
            model_to_dict(new_cf),
            model_to_dict(test_cf)
        )
        self.assertEqual(new_cf.id, test_cf.id)
        self.assertEqual(new_cf.id, 2)
        self.assertEqual(self.f.id, 1)

    def test_functionality_dict_contains_all_functional_groups_as_ratios(self):
        self.assertEqual({u'Out of frame': 0.5, u'Productive': 0.5},
                         self.f.functionality_dict())

    def test_functionality_dict_returns_dict(self):
        self.assertIsInstance(self.f.functionality_dict(), dict)

    def test_j_usage_considers_norm_factor(self):
        cf = ClonoFilter(sample=self.s, norm_factor=2)
        j_usage_dict = cf.j_usage_dict()
        self.assertEqual({u'TRBJ2-4': 0.5, u'TRBJ2-5': 1.5}, j_usage_dict)

    def test_j_usage_dict_returns_dict_indexed_by_j_gene(self):
        j_usage_dict = self.f.j_usage_dict()
        self.assertIsInstance(j_usage_dict, dict)

        self.assertEqual({u'TRBJ2-4': 0.25, u'TRBJ2-5': 0.75}, j_usage_dict)

    def test_v_usage_considers_norm_factor(self):
        cf = ClonoFilter(sample=self.s, norm_factor=2)
        v_usage_dict = cf.v_usage_dict()
        self.assertEqual({u'9': .5, u'8': .5, u'7': 1}, v_usage_dict)

    def test_v_usage_dict_returns_dict_indexed_by_v_family(self):
        v_usage_dict = self.f.v_usage_dict()
        self.assertIsInstance(v_usage_dict, dict)

        self.assertEqual({u'9': 0.25, u'8': 0.25, u'7': 0.5}, v_usage_dict)

    def test_normalization_factor_initializes_to_sum_of_raw_counts(self):
        self.f.save()
        self.assertEqual(self.f.size(), self.f.norm_factor)

    def test_get_recombinations_filters_properly(self):
        self.f.min_length = 40
        self.f.save()
        recombinations = Recombination.objects.filter(cdr3_length__gte=40)
        self.assertEqual(map(repr, recombinations),
                         map(repr, self.f.get_recombinations()))

    def test_given_a_clonofilter_return_a_recombination_queryset(self):
        recombination_qs = self.f.get_recombinations()
        self.assertEqual(map(repr, Recombination.objects.all()),
                         map(repr, recombination_qs))

    def test_count_method_returns_number_of_recombinations(self):
        self.assertEqual(3, self.f.count())

    def test_norm_size_method_returns_normalized_sum_of_copy(self):
        from django.db.models import Sum
        self.f.norm_factor = 10.0
        self.f.save()
        self.assertEqual(.4, self.f.norm_size())

    def test_size_method_returns_sum_of_copy(self):
        from django.db.models import Sum
        self.assertEqual(4, self.f.size())

    def test_default_from_sample_does_not_create_a_default_if_one_exists(self):
        ClonoFilter.default_from_sample(self.s)
        ClonoFilter.default_from_sample(self.s)
        self.assertEqual(1, ClonoFilter.objects.all().count())

    def test_default_from_sample_creates_a_default_clonofilter_if_one_does_not_exist(self):
        cf = ClonoFilter.default_from_sample(self.s)
        self.assertEqual(cf, ClonoFilter.objects.get())

    def test_cdr3_length_sum_utilizes_norm_factor_if_it_exists(self):
        self.f.norm_factor = 10
        norm_cdr3_length_sum = self.f.cdr3_length_sum()
        self.assertEqual([[36, .1], [39, .1], [42, .2]], norm_cdr3_length_sum)

#    def test_clonofilter_

    def test_clonofilter_has_min_and_max_length_as_int(self):
        self.f.min_length = 1
        self.f.max_length = 10
        self.f.save()
        f = ClonoFilter.objects.get()
        self.assertEqual(f.min_length, self.f.min_length)
        self.assertEqual(f.max_length, self.f.max_length)
        self.assertIsInstance(f.min_length, int)
        self.assertIsInstance(f.max_length, int)

    def test_clonofilter_filters_on_min_and_max_length(self):
        filtered_clonotypes = Clonotype.objects.filter(
            recombination__cdr3_length__gte=37,
            recombination__cdr3_length__lte=40)
        self.f.min_length = 37
        self.f.max_length = 40
        self.assertQuerysetEqual(filtered_clonotypes,
                                 map(repr, self.f.get_clonotypes()))

    def test_clonofilter_filters_on_v_family(self):
        filtered_clonotypes = Clonotype.objects.filter(
            recombination__v_family_name=9)
        self.f.v_family_name = 9
        self.f.save()

        self.assertQuerysetEqual(filtered_clonotypes,
                                 map(repr, self.f.get_clonotypes()))

    def test_clonofilter_filters_on_j_gene_name(self):
        filtered_clonotypes = Clonotype.objects.filter(
            recombination__j_gene_name='TRBJ2-4')
        self.f.j_gene_name = 'TRBJ2-4'
        self.f.save()

        self.assertQuerysetEqual(filtered_clonotypes,
                                 map(repr, self.f.get_clonotypes()))

    def test_clonofilter_has_normalization_factor_as_a_float(self):
        self.f.norm_factor = 1
        self.f.save()
        f = ClonoFilter.objects.get()
        self.assertEqual(f.norm_factor, self.f.norm_factor)
        self.assertIsInstance(f.norm_factor, float)

    def test_clonofilter_get_clonotypes_should_not_filter_on_a_parameter_if_it_is_not_included(self):
        try:
            self.f.get_clonotypes()
        except ValueError:
            self.fail('clonofilter.get_clonotypes should not fail if sample exists but no other filtering attributes are given')

    def test_clonofilter_filters_on_min_copy(self):
        min_clonotypes = Clonotype.objects.filter(copy__gte=2)
        self.f.min_copy = 2
        self.assertQuerysetEqual(min_clonotypes,
                                 map(repr, self.f.get_clonotypes()))

    def test_clonofilter_has_min_copy(self):
        self.f.min_copy = 0
        self.assertEqual(0, self.f.min_copy)

    def test_clonofilter_has_sample(self):
        f = ClonoFilter.objects.get()
        self.assertEqual(self.s, self.f.sample)

    def test_vj_counts_dict_returns_a_nested_dict(self):
        '''
        dict should be indexed by:
            dict['v_family']['j_gene'] = count
        '''
        vj_counts = self.f.vj_counts_dict()
        self.assertIsInstance(vj_counts, dict)

        assert(vj_counts)

        for v_family in vj_counts.values():
            self.assertIsInstance(v_family, dict)

        self.assertEqual(vj_counts['9']['TRBJ2-5'], 0.25)

    def test_vj_counts_utilizes_norm_factor_if_it_exists(self):
        self.f.norm_factor = 10
        norm_vj_counts = self.f.vj_counts()
        self.assertEqual(.2, norm_vj_counts[0][0])

    def test_vj_counts_returns_an_empty_2d_list_with_dimensions_len_vfam_by_jgene(self):
        v_family_names = Recombination.v_family_names()
        j_gene_names = Recombination.j_gene_names()
        vj_counts = self.f.vj_counts()
        self.assertEqual(len(v_family_names), len(vj_counts))
        self.assertEqual(len(j_gene_names), len(vj_counts[0]))

    def test_vj_counts_returns_a_2d_list_of_v_j_and_sum_of_copies(self):
        #        from collections import defaultdict
        vj_counts = self.f.vj_counts()
        self.assertIsInstance(vj_counts[0], list)
        self.assertEqual(
            ['[0.5, 0]', '[0, 0.25]', '[0.25, 0]'], map(repr, vj_counts))

    def test_cdr3_length_sum_returns_a_list(self):
        sums = self.f.cdr3_length_sum()
        self.assertIsInstance(sums, list)

    def test_cdr3_length_sum_returns_a_nested_list_of_cdr3_lengths_and_their_counts(self):
        hist = self.f.cdr3_length_sum()
        self.assertEqual([[36, 0.25], [39, .25], [42, 0.5]], hist)

    def test_cdr3_length_sum_should_sort_output_by_cdr3_length(self):
        r = RecombinationFactory(
            cdr3_length=10,
            v_family_name=9,
            v_gene_name='(undefined)',
            v_ties='TRBV7-9',
            d_gene_name='TRBD1-2',
            j_gene_name='TRBJ2-5',
            j_ties='',
            v_deletion=1,
            d5_deletion=4,
            d3_deletion=7,
            j_deletion=3,
            n2_insertion=5,
            n1_insertion=5,
            sequence_status='Out of frame',
            v_index=19,
            n1_index=45,
            n2_index=35,
            d_index=40,
            j_index=50,
            nucleotide='GGACTCGGCCATGTATCTCTGTGCCAGCAGCTTAGGTCCCCTAGCTGAAAAAGAGACCCA',
        )

        ClonotypeFactory(
            sample=self.s,
            recombination=r,
            sequence_id='C0FW0ACXX_1_Patient-15-D_1',
            container='UCSC-Kim-P01-01',
            normalized_frequency=9.336458E-6,
            normalized_copy=1,
            raw_frequency=1.6548345E-5,
            copy=10,
        )

        self.assertEqual(
            [[36, 0.25], [39, 0.25], [42, .5]], self.f.cdr3_length_sum())


class ClonoFilter2ModelTest(TestCase):
    def setUp(self):
        make_fake_patient_with_3_clonotypes()
        self.s = Sample.objects.get()

    def DONTtest_clonofilter2_has_sample(self):
        f = ClonoFilter2(sample=self.s)
        f.save()
        cf2 = ClonoFilter2.objects.get()
        self.assertEqual(self.s, cf2.sample)

    def DONTtest_clonofilter_filters_on_min_copy(self):
        min_clonotypes = Clonotype.objects.filter(copy__gte=2)
        f = ClonoFilter2(sample=self.s, min_copy=2)
        self.assertQuerysetEqual(min_clonotypes,
                                 map(repr, self.f.get_clonotypes()))

    def DONTtest_can_filter_based_on_v_and_j_gene_segment(self):
        self.fail('todo')
