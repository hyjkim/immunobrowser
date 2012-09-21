from django.test import TestCase
from patients.models import Patient
from samples.models import Sample
from clonotypes.models import Clonotype

def make_fake_patient():
  p = Patient()
  p.save()
  s = Sample(patient = p)
  s.save()

  c = Clonotype(
        sample = s,
        sequence_id = 'C0FW0ACXX_1_Patient-15-D_1',
        container = 'UCSC-Kim-P01-01',
        nucleotide = 'GGACTCGGCCATGTATCTCTGTGCCAGCAGCTTAGGTCCCCTAGCTGAAAAAGAGACCCA',
        amino_acid = 'CASSLGPLAEKETQYF',
        normalized_frequency = 9.336458E-6,
        normalized_copy = 2,
        raw_frequency = 1.6548345E-5,
        copy = 2,
        cdr3_length = 42,
        v_family_name = 7,
        v_gene_name = '(undefined)',
        v_ties = 'TRBV7-9',
        d_gene_name = 'TRBD1-2',
        j_gene_name = 'TRBJ2-5',
        j_ties = '',
        v_deletion = 1,
        d_5_deletion = 4,
        d_3_deletion = 7,
        j_deletion = 3,
        n_2_insertion = 5,
        n_1_insertion = 5,
        sequence_status = 'Productive',
        v_index = 19,
        n_1_index = 45,
        n_2_index = 35,
        d_index = 40,
        j_index = 50,
      )
  c.save()


class ClonotypesViewTest(TestCase):
  def test_clonotypes_views_all_renders_all_template(self):
    make_fake_patient()
    response = self.client.get('/samples/1/clonotypes/')
    self.assertTemplateUsed(response, 'all.html')
    pass

class ClonotypeModelTest(TestCase):
  def test_create_clonotypes_for_a_sample(self):
    p = Patient()
    p.save()
    s = Sample(patient = p)
    s.save()

    c = Clonotype(
          sample = s,
          sequence_id = 'C0FW0ACXX_1_Patient-15-D_1',
          container = 'UCSC-Kim-P01-01',
          nucleotide = 'GGACTCGGCCATGTATCTCTGTGCCAGCAGCTTAGGTCCCCTAGCTGAAAAAGAGACCCA',
          amino_acid = 'CASSLGPLAEKETQYF',
          normalized_frequency = 9.336458E-6,
          normalized_copy = 2,
          raw_frequency = 1.6548345E-5,
          copy = 2,
          cdr3_length = 42,
          v_family_name = 7,
          v_gene_name = '(undefined)',
          v_ties = 'TRBV7-9',
          d_gene_name = 'TRBD1-2',
          j_gene_name = 'TRBJ2-5',
          j_ties = '',
          v_deletion = 1,
          d_5_deletion = 4,
          d_3_deletion = 7,
          j_deletion = 3,
          n_2_insertion = 5,
          n_1_insertion = 5,
          sequence_status = 'Productive',
          v_index = 19,
          n_1_index = 45,
          n_2_index = 35,
          d_index = 40,
          j_index = 50,
        )
    c.save()

    # Get all clonotypes from database
    all_clonotypes = Clonotype.objects.all()

    self.assertEqual(all_clonotypes[0], c)



