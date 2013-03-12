from django.test import TestCase
from test_utils.factories import render_echo, FakeRequestFactory
from django.core.urlresolvers import reverse
from mock import patch
from test_utils.ghetto_factory import make_fake_patient_with_3_clonotypes, make_fake_comparison_with_2_samples
from cf_comparisons.models import Comparison
from samples.models import Sample
from cf_comparisons.views import compare, bubble


class ComparisonsViewUnitTest(TestCase):
    '''
    Unit tests of the views patch out the render stack. For
    integration tests, write tests in ComparisonsViewIntegrationTest
    '''
    def setUp(self):
        self.renderPatch = patch('cf_comparisons.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()
        #make_fake_patient_with_3_clonotypes()
        make_fake_comparison_with_2_samples()
        self.comparison = Comparison.objects.get()

    def tearDown(self):
        self.renderPatch.stop()

    def test_compare_view_passes_comparison_instance_to_template_via_context(self):
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual(self.comparison, mock_response.get('comparison'))

    def test_compare_view_passes_list_of_clonofilter_forms_to_template_via_context(self):
        from clonotypes.forms import ClonoFilterForm
        mock_response = compare(self.request, self.comparison.id)
        filter_forms = mock_response.get('filter_forms')
        self.assertIsInstance(filter_forms, list)

        for form in filter_forms:
            self.assertIsInstance(form, ClonoFilterForm)

    def test_compare_view_passes_as_many_forms_as_clonofilters_in_a_comparison_instance(self):
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual(len(self.comparison.clonofilters.all()),
                         len(mock_response.get('filter_forms')))

    def test_compare_uses_compare_html_template(self):
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual('compare.html', mock_response.get('template'))


class ComparisonsViewIntegrationTest(TestCase):
    '''
    For integration tests that require calling the entire django
    stack. Use only when necessary
    '''
    def setUp(self):
        make_fake_comparison_with_2_samples()
        self.comparison = Comparison.objects.get()

    def test_compare_view_contains_a_bubble_image(self):
        response = self.client.get(reverse('cf_comparisons.views.compare',
                                           args=[self.comparison.id]))
        self.assertIn(reverse('cf_comparisons.views.bubble', args=[self.comparison.id]),
                      response.content)

    def test_compare_view_shows_filters_for_all_clonofilters(self):
        clonofilters = self.comparison.clonofilters.all()
        samples = [clonofilter.sample for clonofilter in clonofilters]
        response = self.client.get(reverse('cf_comparisons.views.compare',
                                           args=[self.comparison.id]))
        self.assertIn(str(samples[0]), response.content)


class ComparisonImageTests(TestCase):
    '''
    For testing images generated using a comparison object
    '''

    def setUp(self):
        self.renderPatch = patch('clonotypes.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()
        make_fake_comparison_with_2_samples()
        self.comparison = Comparison.objects.get()

    def tearDown(self):
        self.renderPatch.stop()

    def test_bubble_returns_a_png(self):
        mock_response = bubble(self.request, self.comparison.id)
        self.assertEqual('image/png', mock_response['content-type'])
