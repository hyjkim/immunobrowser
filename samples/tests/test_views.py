from django.test import TestCase
from django.core.urlresolvers import reverse
from test_utils.ghetto_factory import make_fake_patient
from samples.models import Sample
from patients.models import Patient

class SampleViewTest(TestCase):
    ''' Integration tests '''
    def setUp(self):
        make_fake_patient()
        self.s = Sample.objects.get()
        self.p = Patient.objects.get()

    def test_creating_a_sample_generates_a_new_sample_in_database(self):
        all_samples = Sample.objects.all()
        self.assertEquals(len(all_samples), 1)
        self.assertEquals(all_samples[0].id, self.s.id)

    def test_clonotype_summary_contains_link_to_all_clonotypes(self):
        response = self.client.get(
            reverse('samples.views.summary', args=[self.s.id]))
        all_clonotypes_url = reverse('clonotypes.views.all', args=[self.s.id])
        self.assertIn(all_clonotypes_url, response.content)

    def test_clonotype_summary_receives_sample_id(self):
        response = self.client.get(
            reverse('samples.views.summary', args=[self.s.id]))
        sample_in_context = response.context['sample']
        self.assertEqual(sample_in_context.id, self.s.id)

    def test_clonotype_summary_renders_summary_template(self):
        response = self.client.get(
            reverse('samples.views.summary', args=[self.s.id]))
        self.assertTemplateUsed(response, 'summary.html')

    def test_clonotype_summary_passes_sample_to_template(self):
        response = self.client.get(
            reverse('samples.views.summary', args=[self.s.id]))
        sample_in_context = response.context['sample']
        self.assertEqual(sample_in_context, self.s)

    def test_clonotype_summary_displays_patient_and_sample_information(self):
        response = self.client.get(
            reverse('samples.views.summary', args=[self.s.id]))
        self.assertIn(self.p.name, response.content)
        self.assertIn(self.p.disease, response.content)
        self.assertIn("Dec. 12, 2012", response.content)
        self.assertIn(self.s.cell_type, response.content)

    def test_clonotype_summary_displays_bubble_default_plot(self):
        response = self.client.get(
            reverse('samples.views.summary', args=[self.s.id]))
        self.assertIn(reverse('clonotypes.views.bubble_default', args=[self.s.id]), response.content)

    def test_clonotype_summary_displays_spectratype_default_plot(self):
        response = self.client.get(
            reverse('samples.views.summary', args=[self.s.id]))
        self.assertIn(reverse('clonotypes.views.spectratype_default', args=[self.s.id]), response.content)

    def test_samples_url_shows_all_samples(self):
        # Retrieve all saved samples from the database
        all_samples = Sample.objects.all()

        # Get the samples page
        response = self.client.get('/samples/')

        # Make sure we're using the home view
        self.assertTemplateUsed(response, 'home.html')

        # Check we passed the samples to the template
        samples_in_context = response.context['samples']
        self.assertEqual(list(samples_in_context), list(all_samples))

        for sample in all_samples:
            self.assertIn(sample.patient.name, response.content)
            self.assertIn(sample.patient.gender, response.content)
            self.assertIn(sample.patient.disease, response.content)
            #self.assertIn(sample.patient.age(), response.content)
            #self.assertIn(sample.draw_date, response.content)
            self.assertIn(sample.cell_type, response.content)

    def test_samples_have_summary_links_that_redirect_to_clonotype_summary_page(self):
        all_samples = Sample.objects.all()

        # Get the samples page
        response = self.client.get('/samples/')

        # Try to find summary links
        for sample in all_samples:
            sample_url = reverse('samples.views.summary', args=[sample.id])
            self.assertIn(sample_url, response.content)
