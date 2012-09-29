from django.test import TestCase
from patients.models import Patient
from samples.models import Sample
from clonotypes.models import Clonotype
from django.core.urlresolvers import reverse

def make_fake_patient():
  p = Patient(name = 'test patient',)
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
        d5_deletion = 4,
        d3_deletion = 7,
        j_deletion = 3,
        n2_insertion = 5,
        n1_insertion = 5,
        sequence_status = 'Productive',
        v_index = 19,
        n1_index = 45,
        n2_index = 35,
        d_index = 40,
        j_index = 50,
      )
  c.save()


class ClonotypesViewTest(TestCase):
  def test_clonotypes_views_all_renders_all_template(self):
    make_fake_patient()
    fake_sample = Sample.objects.get()
    response = self.client.get(reverse ('samples.views.summary', args=[fake_sample.id]))
    self.assertTemplateUsed(response, 'summary.html')

  def test_clonotypes_all_view_shows_summary_template(self):
    make_fake_patient()
    fake_sample = Sample.objects.get()
    response = self.client.get(reverse ('samples.views.summary', args=[fake_sample.id]))

    self.assertIn('test patient', response.content)

  def test_clonotypes_all_view_passes_clonotypes_to_template(self):
    make_fake_patient()
    fake_sample = Sample.objects.get()
    fake_clonotypes = Clonotype.objects.filter(id=fake_sample.id)
    response = self.client.get(reverse ('samples.views.summary', args=[fake_sample.id]))
    clonotypes_in_context = response.context['clonotypes']
    self.assertEqual(clonotypes_in_context, fake_clonotypes)

  def test_clonotypes_all_view_passes_sample_to_template(self):
    make_fake_patient()
    fake_sample = Sample.objects.get()
    response = self.client.get(reverse ('samples.views.summary', args=[fake_sample.id]))
    sample_in_context = response.context['sample']
    self.assertEqual(sample_in_context, fake_sample)


