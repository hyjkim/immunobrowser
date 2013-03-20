from patients.models import Patient
from samples.models import Sample
from clonotypes.models import Clonotype
from cf_comparisons.models import Comparison
from test_utils.factories import ClonotypeFactory


# These functions should eventually be replaced by factories
def make_fake_patient():
    ClonotypeFactory()


def make_fake_patient_with_2_clonotypes():
    make_fake_patient()
    s = Sample.objects.get()
    c2 = ClonotypeFactory(
        sample=s,
        nucleotide='TGGACTCGGCCATGTATCTCTGTGCCAGCAGCTTAGGTCCCCTAGCTGAAAAAGAGACCCA',
        amino_acid='',
        copy=1,
        cdr3_length=39,
        v_family_name=8,
        v_gene_name='(undefined)',
        v_ties='',
        j_gene_name='TRBJ2-4',
        sequence_status='Out of frame',
    )


def make_fake_patient_with_3_clonotypes():
    make_fake_patient_with_2_clonotypes()
    s = Sample.objects.get()
    c2 = ClonotypeFactory(
        sample=s,
        nucleotide='CGGACTCGGCCATGTATCTCTGTGCCAGCAGCTTAGGTCCCCTAGCTGAAAAAGAGACCCA',
        amino_acid='',
        normalized_copy=1,
        copy=1,
        cdr3_length=36,
        v_family_name=9,
        sequence_status='Out of frame',
    )


def make_fake_comparison_with_2_samples():
    make_fake_patient_with_2_clonotypes()
    p = Patient.objects.get()
    s1 = Sample.objects.get()
    s2 = Sample(patient=p, draw_date='2012-12-13', cell_type='cd4+')
    s2.save()

    c = Clonotype(
        sample=s2,
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

    Comparison.default_from_samples([s1, s2])
