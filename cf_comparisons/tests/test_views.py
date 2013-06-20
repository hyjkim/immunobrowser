from django.test import TestCase
from test_utils.factories import render_echo, FakeRequestFactory
from django.core.urlresolvers import reverse
from mock import patch
from test_utils.ghetto_factory import make_fake_comparison_with_2_samples
from cf_comparisons.models import Comparison
from samples.models import Sample
from cf_comparisons.views import compare, bubble, sample_compare
from cf_comparisons.forms import SampleCompareForm


class ComparisonsViewUnitTest(TestCase):
    '''
    Unit tests of the views patch out the render stack. For
    integration tests, write tests in ComparisonsViewIntegrationTest
    '''
    def setUp(self):
        self.renderPatch = patch('cf_comparisons.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()
        make_fake_comparison_with_2_samples()
        self.comparison = Comparison.objects.get()

    def tearDown(self):
        self.renderPatch.stop()

    def test_compare_sends_shared_amino_acids_and_related_clonotypes(self):
        mock_response = compare(self.request, self.comparison.id)
        self.assertEquals('', mock_response.get('shared_amino_acids'))

    def test_compare_should_pass_samples_to_template_via_context(self):
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual(self.comparison.get_samples(
        ), mock_response.get('samples'))

    def test_compare_should_pass_shared_clonotypes_to_template_via_context(self):
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual(self.comparison.get_shared_amino_acids_clonotypes(
        ), mock_response.get('shared_clonotypes'))

    def test_compare_should_pass_num_forms_to_template_via_context(self):
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual(2, mock_response.get('num_forms'))

    def test_clonofilter_forms_in_compare_should_have_prefixes(self):
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual('0', mock_response.get('filter_forms')[0].prefix)

    def test_sample_compare_view_passes_sample_compare_form_to_template_via_context(self):
        '''
        Make sure the compare samples view is getting passed the compare sample form
        '''
        mock_response = sample_compare(self.request)
        self.assertIsInstance(
            mock_response.get('sample_compare_form'), SampleCompareForm)

    def test_sample_compare_renders_sample_compare_template(self):
        mock_response = sample_compare(self.request)
        self.assertEqual('sample_compare.html', mock_response.get('template'))

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

    def test_compare_renders_compare_html_template(self):
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

    def DONTtest_clonotype_tracking_view_reads_comparison_and_amino_acid_sequences_from_post(self):
        self.fail('todo')

    def test_compare_view_shows_sample_name_in_header_of_shared_clonotype_table(self):
        response = self.client.get(reverse('cf_comparisons.views.compare',
                                           args=[self.comparison.id]))
        self.fail('todo')

    def test_compare_view_contains_a_combined_spectratype(self):
        response = self.client.get(reverse('cf_comparisons.views.compare',
                                           args=[self.comparison.id]))
        self.assertIn(
            reverse('cf_comparisons.views.spectratype', args=[
                    self.comparison.id]),
            response.content)

    def test_comparison_has_links_to_clonofilters_within_comparison(self):
        response = self.client.get(
            reverse('cf_comparisons.views.compare', args=[self.comparison.id]))
        for clonofilter in self.comparison.clonofilters.all():
            url = "%s?clonofilter=%d" % (reverse('samples.views.summary', args=[clonofilter.sample.id]), clonofilter.id)
            self.assertIn(url, response.content)

    def test_comparison_view_shows_a_table_of_raw_and_normalized_sample_sizes(self):
        response = self.client.get(
            reverse('cf_comparisons.views.compare', args=[self.comparison.id]))
        self.assertIn("Number of Recombinations", response.content)
        self.assertIn("Raw Counts", response.content)
        self.assertIn("Normalized Counts", response.content)
        for clonofilter in self.comparison.clonofilters.all():
            self.assertIn(str(clonofilter.sample), response.content)

    def test_compare_shared_clonotypes_should_link_to_clonotype_detail(self):
        from clonotypes.models import Clonotype
        response = self.client.get(
            reverse('cf_comparisons.views.compare', args=[self.comparison.id]))
        samples = self.comparison.get_samples()
        self.assertEqual('', response.context['shared_clonotypes'])
#        self.assertIn(reverse('clonotypes.views.detail', args=[self.comparison.id]),response.content)
        self.fail('todo')

    def test_compare_shows_links_to_shared_amino_acid(self):
        from clonotypes.models import AminoAcid
        response = self.client.get(
            reverse('cf_comparisons.views.compare', args=[self.comparison.id]))
        aa = self.comparison.get_shared_amino_acids()[0]
        self.assertIn(reverse('clonotypes.views.amino_acid_detail',
                      args=[aa.id]), response.content)

    def test_compare_shows_shared_clonotypes_as_table(self):
        response = self.client.get(
            reverse('cf_comparisons.views.compare', args=[self.comparison.id]))
        self.assertIn('td class="clonotype"', response.content)

    def test_compare_should_have_number_of_forms_as_hidden_field(self):
        response = self.client.get(
            reverse('cf_comparisons.views.compare', args=[self.comparison.id]))
        self.assertIn('<input type="hidden" name="num_forms" value="2">',
                      response.content)

    def test_compare_creates_a_new_comparison_if_filter_form_is_changed(self):
        samples = Sample.objects.all()
        clonofilters = {'0-sample': samples[0].id,
                        '1-sample': samples[1].id,
                        '0-min_length': 1,
                        'num_forms': 2}
        self.client.post(reverse('cf_comparisons.views.compare',
                         args=[self.comparison.id]), clonofilters)
        self.assertEqual(2, Comparison.objects.all().count())

    def DONTtest_compare_should_redirect_to_comparison_defined_in_posted_clonofilterforms(self):
        response = self.client.post(reverse(
            'cf_comparisons.views.compare', args=[self.comparison.id]), {})
        self.assertRedirects(response, '/compare/1')

    def test_sample_compare_uses_a_template_tag(self):
        from django.template import Template, Context
        t = Template('{% load comparison_tags %}{% sample_compare_tag sample_compare_form %}')
        c = Context({'sample_compare_form': None})
        self.assertIn('<form action=', t.render(c))

    def test_sample_compare_redirects_to_compare_view_after_post(self):
        sample_ids = [sample.id for sample in Sample.objects.all()]
        comparison = Comparison.default_from_samples(Sample.objects.all())
        response = self.client.post(
            reverse('cf_comparisons.views.sample_compare'),
            {'samples': sample_ids})
        self.assertRedirects(response,
                             reverse('cf_comparisons.views.compare', args=[comparison.id]))

    def test_sample_compare_view_has_submit_button(self):
        response = self.client.get(
            reverse('cf_comparisons.views.sample_compare'))
        self.assertIn('<input type="submit" />', response.content)

    def test_sample_compare_view_renders_samples(self):
        response = self.client.get(
            reverse('cf_comparisons.views.sample_compare'))
        for sample in Sample.objects.all():
            self.assertIn(str(sample), response.content)

    def test_compare_view_contains_a_bubble_image(self):
        response = self.client.get(reverse('cf_comparisons.views.compare',
                                           args=[self.comparison.id]))
        self.assertIn(
            reverse('cf_comparisons.views.bubble', args=[self.comparison.id]),
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
