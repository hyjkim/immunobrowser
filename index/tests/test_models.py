from django.test import TestCase
from test_utils.ghetto_factory import make_fake_patient_with_3_clonotypes
from test_utils.factories import SampleFactory, ClonotypeFactory
from samples.models import Sample
from index.models import SampleToAmino
from clonotypes.models import AminoAcid

class SampleToAminoModelTest(TestCase):

    def test_SampleToAmino_get_or_create_does_not_create_every_call(self):
        ClonotypeFactory()
        s = Sample.objects.get()
        self.assertEqual(0, len(SampleToAmino.objects.all()))
        s2a, created = SampleToAmino.objects.get_or_create(sample=s)
        self.assertEqual(1, len(SampleToAmino.objects.all()))
        self.assertEqual(True, created)
        s2a2, created2 = SampleToAmino.objects.get_or_create(sample=s)
        self.assertEqual(False, created2)

    def test_SampleToAmino_returns_only_aminos_belonging_to_a_patient(self):
        ClonotypeFactory()
        s = Sample.objects.get()
        aa_keys = [aa.id for aa in AminoAcid.objects.all()]
        ClonotypeFactory()
        s2a = SampleToAmino(sample=s)
        s2a.save()
        self.assertEquals(aa_keys, s2a.amino_acids)

    def test_SampleToAmino_update_stores_amino_acid_keys_as_json_in_db(self):
        make_fake_patient_with_3_clonotypes()
        s = Sample.objects.get()
        s2a = SampleToAmino(sample=s)
        s2a.save()
        self.assertEquals('[1, 2, 3]', s2a._amino_acids)

    def test_SampleToAmino_amino_acids_returns_list_of_keys_if_amino_acids_exist_when_created(self):
        make_fake_patient_with_3_clonotypes()
        s = Sample.objects.get()
        s2a = SampleToAmino(sample=s)
        s2a.save()
        aa_keys = [aa.id for aa in AminoAcid.objects.all()]
        self.assertEquals(aa_keys, s2a.amino_acids)

    def test_SampleToAmino_amino_acids_returns_empty_list_if_update_has_not_been_called(self):
        s = SampleFactory()
        s2a = SampleToAmino(sample=s)
        s2a.save()
        self.assertEquals([], s2a.amino_acids)

    def test_SampleToAmino_model_contains_a_sample(self):
        ClonotypeFactory()
        s = Sample.objects.get()
        s2a = SampleToAmino(sample=s)
        self.assertEqual(s, s2a.sample)
