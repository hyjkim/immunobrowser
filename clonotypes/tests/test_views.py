from django.test import TestCase
from patients.models import Patient
from samples.models import Sample
from clonotypes.models import Clonotype
from django.core.urlresolvers import reverse
from shared_methods import make_fake_patient, make_fake_patient_with_3_clonotypes


class ClonotypesViewTest(TestCase):
    def test_clonotypes_views_all_renders_all_template(self):
        make_fake_patient()
        fake_sample = Sample.objects.get()
        response = self.client.get(
            reverse('clonotypes.views.all', args=[fake_sample.id]))
        self.assertTemplateUsed(response, 'all.html')

    def test_clonotypes_all_view_shows_summary_template(self):
        make_fake_patient()
        fake_sample = Sample.objects.get()
        response = self.client.get(
            reverse('clonotypes.views.all', args=[fake_sample.id]))

        self.assertIn('test patient', response.content)

    def test_clonotypes_all_view_passes_clonotypes_to_template(self):
        self.assertEqual(0, len(Sample.objects.all()))
        make_fake_patient_with_3_clonotypes()
        fake_sample = Sample.objects.get()
        fake_clonotypes = Clonotype.objects.filter(sample=fake_sample)
        response = self.client.get(
            reverse('clonotypes.views.all', args=[fake_sample.id]))
        clonotypes_in_context = response.context['clonotypes']
# Comparing querysets may be less messy by monkeypatching TestCase with
# assertEqualQueryset. Check http://djangosnippets.org/snippets/2013/
        pk = lambda o: o.pk
        self.assertEqual(list(sorted(fake_clonotypes, key=pk)),
                         list(sorted(clonotypes_in_context, key=pk)))

    def test_clonotypes_all_view_passes_sample_to_template(self):
        make_fake_patient()
        fake_sample = Sample.objects.get()
        response = self.client.get(
            reverse('clonotypes.views.all', args=[fake_sample.id]))
        sample_in_context = response.context['sample']
        self.assertEqual(sample_in_context, fake_sample)
