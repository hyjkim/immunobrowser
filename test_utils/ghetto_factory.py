from patients.models import Patient
from samples.models import Sample
from clonotypes.models import Clonotype
from cf_comparisons.models import Comparison
from test_utils.factories import ClonotypeFactory, RecombinationFactory



# These functions should eventually be replaced by factories
def make_fake_patient():
    ClonotypeFactory()

def make_fake_patient_with_2_clonotypes():
    make_fake_patient()
    s = Sample.objects.get()
    r = RecombinationFactory(
        nucleotide='TGGACTCGGCCATGTATCTCTGTGCCAGCAGCTTAGGTCCCCTAGCTGAAAAAGAGACCCA',
        cdr3_length=39,
        j_gene_name='TRBJ2-4',
        sequence_status='Out of frame',
    )

    ClonotypeFactory(
        sample=s,
        recombination=r,
        count=1,
    )


def make_fake_patient_with_3_clonotypes():
    make_fake_patient_with_2_clonotypes()
    s = Sample.objects.get()
    r = RecombinationFactory(
        cdr3_length=36,
        sequence_status='Out of frame',
        v_gene_name='TRBV1-1',
        nucleotide='CGGACTCGGCCATGTATCTCTGTGCCAGCAGCTTAGGTCCCCTAGCTGAAAAAGAGACCCA',
    )

    ClonotypeFactory(
        sample=s,
        recombination=r,
        count=1,
    )


def make_fake_comparison_with_2_samples():
    from clonotypes.models import AminoAcid
    make_fake_patient_with_2_clonotypes()
    p = Patient.objects.get()
    s1 = Sample.objects.get()
    s2 = Sample(patient=p, draw_date='2012-12-13', cell_type='cd4+')
    s2.save()

    # Make sure there's an overlapping amino_acid here
    aa = AminoAcid.objects.all()[0]
    r = aa.recombination_set.all()[0]

    c = ClonotypeFactory(
        sample=s2,
        recombination = r
    )

    Comparison.default_from_samples([s1, s2])
