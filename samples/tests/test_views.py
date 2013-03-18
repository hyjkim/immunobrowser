from django.test import TestCase
from django.core.urlresolvers import reverse
from test_utils.ghetto_factory import make_fake_patient
from samples.models import Sample
from samples.views import summary
from patients.models import Patient
from test_utils.factories import render_echo, FakeRequestFactory
from mock import MagicMock, patch, call
from clonotypes.models import ClonoFilter
from clonotypes.forms import ClonoFilterForm
from django.forms.models import model_to_dict


class SampleMockedViewTest(TestCase):
    ''' Here, we mock out the rendering stack for fast unit tests of the view'''

    def setUp(self):
        self.renderPatch = patch('samples.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()
        make_fake_patient()
        self.s = Sample.objects.get()

    def tearDown(self):
        self.renderPatch.stop()

    def test_samples_summary_with_no_clonofiliter_in_post_or_get_serves_an_initialized_default_clonofilter(self):
        mock_response = summary(self.request, self.s.id)
        self.assertEqual(
            mock_response.get('clonofilter').id, 1)

    def test_samples_summary_passes_clonofilter_form_to_context(self):
        mock_response = summary(self.request, self.s.id)
        self.assertIsInstance(
            mock_response.get('filter_form'), ClonoFilterForm)

    def test_summary_should_try_to_read_in_clonofilter_from_get(self):
        cf = ClonoFilter(sample=self.s)
        cf.save()

        self.request = FakeRequestFactory(GET={'clonofilter': cf.id})
        mock_response = summary(self.request, self.s.id)
        self.assertEqual(mock_response.get('clonofilter'), cf)

        cf2 = ClonoFilter(sample=self.s)
        cf2.save()

        self.request = FakeRequestFactory(GET={'clonofilter': cf2.id})
        mock_response = summary(self.request, self.s.id)
        self.assertEqual(mock_response.get('clonofilter'), cf2)

    def test_summary_should_fill_out_form_if_clonofilter_is_passed_through_get(self):
        cf = ClonoFilter(sample=self.s, min_copy=10)
        cf.save()
        self.request = FakeRequestFactory(GET={'clonofilter': cf.id})
        mock_response = summary(self.request, self.s.id)
#        self.assertEqual({'min_copy': 10, 'sample': 1},
#                         mock_response.get('filter_form').initial)
        self.assertEqual(
            10, mock_response.get('filter_form').initial['min_copy'])
        self.assertEqual(1, mock_response.get('filter_form').initial['sample'])


class SampleViewIntegrationTest(TestCase):
    ''' Integration tests '''
    def setUp(self):
        make_fake_patient()
        self.s = Sample.objects.get()
        self.p = Patient.objects.get()

    def test_summary_should_redirect_if_a_new_sample_is_provided_in_form(self):
        s2 = Sample(patient=self.p,cell_type="t", draw_date='1999-11-11')
        s2.save()
        url = "%s?clonofilter=1" % reverse('samples.views.summary', args=[s2.id])
        self.assertRedirects(self.client.post(reverse('samples.views.summary', args=[self.s.id]),
                                              {'sample': s2.id}), url)

    def test_summary_clonofilter_id_bubble(self):
        cf = ClonoFilter(sample=self.s)
        cf.save()
        url = "%s?clonofilter=%s" % (
            reverse('samples.views.summary', args=[self.s.id]), cf.id)
        bubble_url = "%s?clonofilter=%s" % (
            reverse('clonotypes.views.bubble_default', args=[self.s.id]), cf.id)
        response = self.client.get(url)
        self.assertIn(bubble_url, response.content)

    def test_summary_should_redirect_to_default_summary_if_clonofilter_id_does_not_exist(self):
        url = "%s?clonofilter=%s" % (
            reverse('samples.views.summary', args=[self.s.id]), 100000)
        response = self.client.get(url)
        self.assertRedirects(
            response, reverse('samples.views.summary', args=[self.s.id]))

    def test_sample_summary_redirects_post_request_to_url_with_clonofilter(self):
        response = self.client.post(
            reverse('samples.views.summary', args=[self.s.id]), {'sample': 1, 'min_copy': 10})
        cf = ClonoFilter.objects.get()
        url = "%s?clonofilter=%s" % (
            reverse('samples.views.summary', args=[self.s.id]), cf.id)
        self.assertRedirects(response, url)

    def test_sample_summary_redirects_on_post_request(self):
        response = self.client.post(
            reverse('samples.views.summary', args=[self.s.id]), {'sample': 1})
        self.assertRedirects(
            response, 'http://testserver/samples/1?clonofilter=1')

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
        self.assertIn(reverse('clonotypes.views.bubble_default',
                      args=[self.s.id]), response.content)

    def test_clonotype_summary_displays_spectratype_default_plot(self):
        response = self.client.get(
            reverse('samples.views.summary', args=[self.s.id]))
        self.assertIn(reverse('clonotypes.views.spectratype_default',
                      args=[self.s.id]), response.content)

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

    def test_samples_summary_shows_filter_form_sample_id(self):
        response = self.client.get(
            reverse('samples.views.summary', args=[self.s.id]))
        self.assertIn('id_sample', response.content)

    def test_samples_summary_shows_submit_button_for_sample_id(self):
        response = self.client.get(
            reverse('samples.views.summary', args=[self.s.id]))
        self.assertIn('<input type="submit" />', response.content)
