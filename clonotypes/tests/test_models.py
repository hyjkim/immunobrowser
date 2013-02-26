from django.test import TestCase
from patients.models import Patient
from samples.models import Sample
from clonotypes.models import Clonotype
from test_utils.ghetto_factory import make_fake_patient, make_fake_patient_with_3_clonotypes


class ClonotypeModelTest(TestCase):
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

        c = Clonotype(
            sample=s,
            sequence_id='C0FW0ACXX_1_Patient-15-D_1',
            container='UCSC-Kim-P01-01',
            nucleotide='GGACTCGGCCATGTATCTCTGTGCCAGCAGCTTAGGTCCCCTAGCTGAAAAAGAGACCCA',
            amino_acid='CASSLGPLAEKETQYF',
            normalized_frequency=9.336458E-6,
            normalized_copy=2,
            raw_frequency=1.6548345E-5,
            copy=2,
            cdr3_length=42,
            v_family_name=7,
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
            sequence_status='Productive',
            v_index=19,
            n1_index=45,
            n2_index=35,
            d_index=40,
            j_index=50,
        )
        c.save()

        # Get all clonotypes from database
        all_clonotypes = Clonotype.objects.all()

        self.assertEqual(all_clonotypes[0], c)

#    def test_vj_usage_returns_double_array(self):
#        s = Sample.objects.get()
#        self.assertEqual("",vj_usage(s))

    def test_v_family_names_returns_list_of_distinct_v_family_names(self):
        make_fake_patient_with_3_clonotypes()
        self.assertIsInstance(Clonotype.v_family_names(), list)
        self.assertEqual(['7', '8', '9'], Clonotype.v_family_names())

    def test_j_gene_names_returns_list_of_distinct_j_gene_names(self):
        make_fake_patient_with_3_clonotypes()
        self.assertIsInstance(Clonotype.j_gene_names(), list)
        self.assertEqual([u'TRBJ2-5', u'TRBJ2-4'], Clonotype.j_gene_names())


from clonotypes.models import ClonoFilter


class ClonoFilterModelTest(TestCase):

    def test_clonofilter_get_clonotypes_should_not_filter_on_a_parameter_if_it_is_not_included(self):
        self.fail('Todo this')

    def test_clonofilter_filters_on_min_copy(self):
        make_fake_patient_with_3_clonotypes()
        s = Sample.objects.get()
        f = ClonoFilter(sample=s, min_copy=2)
        min_clonotypes = Clonotype.objects.filter(copy__gte=2)
        self.assertQuerysetEqual(min_clonotypes,
                                 map(repr, f.get_clonotypes()))

    def test_clonofilter_has_min_copy(self):
        f = ClonoFilter()
        f.min_copy = 0
        self.assertEqual(0, f.min_copy)

    def test_clonofilter_has_sample(self):
        make_fake_patient()
        s = Sample.objects.get()
        tmp = ClonoFilter()
        tmp.sample = s
        tmp.save()

        f = ClonoFilter.objects.get()
        self.assertEqual(s, f.sample)

    def test_vj_counts_returns_an_empty_2d_list_with_dimensions_len_vfam_by_jgene(self):
#        from collections import defaultdict
        make_fake_patient_with_3_clonotypes()
        s = Sample.objects.get()
        f = ClonoFilter(sample=s, min_copy=4)
        v_family_names = Clonotype.v_family_names()
        j_gene_names = Clonotype.j_gene_names()
        vj_counts = f.vj_counts()
        self.assertEqual(len(v_family_names), len(vj_counts))
        self.assertEqual(len(j_gene_names), len(vj_counts[0]))

    def test_vj_counts_returns_a_2d_list_of_v_j_and_sum_of_copies(self):
#        from collections import defaultdict
        make_fake_patient_with_3_clonotypes()
        s = Sample.objects.get()
        f = ClonoFilter(sample=s, min_copy=0)
        vj_counts = f.vj_counts()
        self.assertIsInstance(vj_counts[0], list)
        self.assertEqual(['[2, 0]', '[0, 1]', '[1, 0]'], map(repr, vj_counts))
