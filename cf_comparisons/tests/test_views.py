from django.test import TestCase
from test_utils.factories import render_echo, FakeRequestFactory, ComparisonFactory
from django.core.urlresolvers import reverse
from mock import patch
from test_utils.ghetto_factory import make_fake_comparison_with_2_samples
from cf_comparisons.models import Comparison
from samples.models import Sample
from cf_comparisons.views import compare, bubble, sample_compare, scatter_nav, shared_clones, background_colors, compare_v3, add_samples_v2
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

    def test_shared_clones_ajax_has_a_url(self):
        self.assertTrue(reverse('cf_comparisons.views.shared_clones_ajax', args=[self.comparison.id]))

    def test_functionality_ajax_has_a_url(self):
        self.assertEqual('/compare/1/functionality_ajax',
                reverse('cf_comparisons.views.functionality_ajax', args=[self.comparison.id]))

    def test_functionality_ajax_returns_functionality_stats(self):
        from cf_comparisons.views import functionality_ajax
        self.assertEqual('{"sampleNames": {"1": "test patient 2012-12-12 cd4+", "2": "test patient 2012-12-13 cd4+"}, "functionality": [{"values": {"Out of frame": 0.3333333333333333, "Productive": 0.6666666666666666}, "key": 1}, {"values": {"Productive": 1.0}, "key": 2}]}',
                         functionality_ajax(self.request, self.comparison.id).content)

    def DONTtest_update_clonofilters_takes_in_serialized_json_from_post_and_returns_a_new_comparison_id(self):
        from cf_comparisons.views import update_clonofilters
        from cf_comparisons.forms import ClonoFilterForm
        data = {};
        self.request.post = data;
        self.assertEqual('2',
                update_clonofilters(self.request, self.comparison.id).content)

    def test_update_clonofilters_has_a_url(self):
        self.assertEqual(
                '/compare/1/update_clonofilters',
                reverse('cf_comparisons.views.update_clonofilters', args=[self.comparison.id]))

    def test_clonofilter_colors_has_a_url(self):
        self.assertEqual('/compare/1/clonofilter_colors',
                reverse('cf_comparisons.views.clonofilter_colors', args=[self.comparison.id]))

    def test_clonofilter_colors_returns_colors_for_comparison(self):
        from cf_comparisons.views import clonofilter_colors
        self.assertIn(
                '.cf-1.active { background-color: rgba(255, 0, 41, 0.75)}',
                clonofilter_colors(self.request, self.comparison.id).content)

    def test_vj_freq_ajax_returns_vj_usage_sample_stats(self):
        from cf_comparisons.views import vj_freq_ajax
        self.assertEqual(
                '{"vjFreq": [["TRBV25-1", "TRBJ1-1", 0.6666666666666666, 1], ["TRBV25-1", "TRBJ2-4", 0.3333333333333333, 1], ["TRBV25-1", "TRBJ1-1", 1.0, 2]], "sampleNames": {"1": "test patient 2012-12-12 cd4+", "2": "test patient 2012-12-13 cd4+"}, "jList": ["TRBJ1-1", "TRBJ2-4"], "vList": ["TRBV25-1"]}',
                vj_freq_ajax(self.request, self.comparison.id).content)

    def test_compare_v3_renders_compare_v3_html(self):
        response = compare_v3(self.request, self.comparison.id)
        self.assertEqual('compare_v3.html', response['template'])

    def test_compare_v3_returns_comparison_to_template(self):
        response = compare_v3(self.request, self.comparison.id)
        self.assertEqual(self.comparison, response['comparison'])

    def test_shared_clones_takes_in_comparison_id(self):
        shared_clones(self.request, self.comparison.id)

    def test_scatter_nav_renders_scatter_nav_template(self):
        from django.template import Template, Context
        response = scatter_nav(self.request, None)
        self.assertEqual(response['template'], 'scatter_nav.html')

    def test_compare_sends_shared_amino_acids_and_related_clonotypes(self):
        mock_response = compare(self.request, self.comparison.id)
        shared_amino_acids = self.comparison.get_shared_amino_acids_related()
        self.assertEquals(
            shared_amino_acids, mock_response.get('shared_amino_acids'))

    def test_compare_should_pass_samples_to_template_via_context(self):
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual(self.comparison.get_samples(
        ), mock_response.get('samples'))

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

    def test_compare_renders_compare_html_template(self):
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual('compare.html', mock_response.get('template'))

    def test_compare_returns_ajax_view_if_request_is_ajax(self):
        self.request.is_ajax = lambda: True
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual('compare_ajax.html', mock_response.get('template'))

    def test_filter_forms_renders_using_filter_form_template(self):
        from cf_comparisons.views import filter_forms
        mock_response = filter_forms(self.request, self.comparison.id)
        self.assertEqual('filter_forms.html', mock_response.get('template'))


class ComparisonsViewIntegrationTest(TestCase):
    '''
    For integration tests that require calling the entire django
    stack. Use only when necessary
    '''
    def setUp(self):
        make_fake_comparison_with_2_samples()
        self.comparison = Comparison.objects.get()

    def test_remove_clonofilter_removes_a_clonofilter_from_a_comparison(self):
        comp = ComparisonFactory()
        cfs = list(comp.clonofilters_all())
        del_cf = cfs.pop()

        url = reverse('cf_comparisons.views.remove_clonofilter')
        post_data = {'comparison': comp.id, 'clonofilter': del_cf.id}
        response = self.client.post(url, data=post_data)
        self.assertNotEqual(comp.id, response.content)
        new_comp = Comparison.objects.get(id=response.content)
        self.assertEqual([cf.id for cf in cfs], [cf.id for cf in new_comp.clonofilters_all()])

    def DONTtest_clonotype_tracking_view_reads_comparison_and_amino_acid_sequences_from_post(self):
        self.fail('todo')

    def DONTtest_compare_view_shows_sample_name_in_header_of_shared_clonotype_table(self):
        response = self.client.get(reverse('cf_comparisons.views.compare',
                                           args=[self.comparison.id]))
        self.fail('todo')

    def DONTtest_compare_view_contains_a_combined_spectratype(self):
        response = self.client.get(reverse('cf_comparisons.views.compare',
                                           args=[self.comparison.id]))
        self.assertIn(
            reverse('cf_comparisons.views.spectratype', args=[
                    self.comparison.id]),
            response.content)

    def test_comparison_view_renders_comparison_template(self):
        from test_utils.ghetto_factory import make_fake_comparison_with_2_samples
        from cf_comparisons.models import Comparison
        comparison = Comparison.objects.get()
        response = self.client.get(reverse('dashboard.views.dashboard_comparison', args=[comparison.id]))
        self.assertTemplateUsed(response, 'dashboard_comparison.html')

    def test_add_samples_v2_does_not_create_a_new_clonofilter_if_new_parameters_are_not_passed(self):
        self.fail('todo: highest priority')

    def test_add_samples_v2_adds_new_samples_to_existing_in_comparison_and_returns_new_comp_id(self):
        from test_utils.factories import SampleFactory
        comp = ComparisonFactory()
        sample = SampleFactory()

        old_cfs = comp.clonofilters_all()
        old_sample_set = set([cf.sample for cf in comp.clonofilters_all()])

        url = reverse('cf_comparisons.views.add_samples_v2')
        post_data = {'comparison': comp.id, 'samples': [sample.id]}
        response = self.client.post(url,
                                    data=post_data)

        new_comp_id = response.content
        new_comp = Comparison.objects.get(id=new_comp_id)
        new_sample_set = set([cf.sample for cf in new_comp.clonofilters_all()])
        self.assertTrue(sample in new_sample_set)
        self.assertEqual(old_sample_set, new_sample_set)
        self.assertTrue(old_sample_set.issubset(new_sample_set))

    def test_shared_clone_view_renders_the_same_as_template_tag(self):
        from django.template import Template, Context
        t = Template(
            '{% load comparison_tags %}{% shared_clones_tag comparison %}')
        c = Context({'comparison': self.comparison})
        url = reverse('cf_comparisons.views.shared_clones', args=[1])
        response = self.client.get(url)
        self.assertIn(t.render(c), response.content)

    def test_scatter_nav_uses_a_template_tag(self):
        from django.template import Template, Context
        t = Template(
            '{% load comparison_tags %}{% scatter_nav_tag comparison %}')
        c = Context({'comparison': self.comparison})
        self.assertIn('<div id="scatter-main"', t.render(c))

    def test_shared_clone_view_has_a_url(self):
        url = reverse('cf_comparisons.views.shared_clones', args=[1])
        self.assertEqual(url, '/compare/1/shared_clones')

    def test_scatter_nav_has_a_url(self):
        url = reverse('cf_comparisons.views.scatter_nav', args=[1])
        self.assertEqual(url, '/compare/1/scatter_nav')

    def test_scatter_nav_has_a_url(self):
        url = reverse('cf_comparisons.views.scatter_nav')
        self.assertEqual(url, '/compare/scatter_nav')

    def test_update_view_takes_in_a_dict_with_string_ids_from_post_and_returns_a_new_comparison_id(self):
        import json
        url = reverse('cf_comparisons.views.update', args=[self.comparison.id])
        cfs = self.comparison.clonofilters_all()

        update_dict = {}
        for cf in cfs:
            update_dict[str(cf.id)] = {'j_gene_name': 'TRBJ2-1'}

        response = self.client.post(url, {'update': json.dumps(update_dict)})
        self.assertNotEqual(str(self.comparison.id), response)
        self.assertEqual(response.content, '2')

    def test_update_view_takes_in_a_request_from_post_and_returns_json_with_comparison_id(self):
        import json
        url = reverse('cf_comparisons.views.update', args=[self.comparison.id])
        cfs = self.comparison.clonofilters_all()

        update_dict = {}
        for cf in cfs:
            update_dict[cf.id] = {'j_gene_name': 'TRBJ2-1'}

        response = self.client.post(url, {'update': json.dumps(update_dict)})
        self.assertNotEqual(str(self.comparison.id), response)
        self.assertEqual(response.content, '2')

    def test_comparison_view_shows_a_table_of_raw_and_normalized_sample_sizes(self):
        response = self.client.get(
            reverse('cf_comparisons.views.compare', args=[self.comparison.id]))
        self.assertIn("Number of Recombinations", response.content)
        self.assertIn("Raw Counts", response.content)
        self.assertIn("Normalized Counts", response.content)
        for clonofilter in self.comparison.clonofilters_all():
            self.assertIn(str(clonofilter.sample), response.content)

    def test_compare_shared_clonotypes_should_link_to_clonotype_detail(self):
        from clonotypes.models import Clonotype
        response = self.client.get(
            reverse('cf_comparisons.views.compare', args=[self.comparison.id]))
        samples = self.comparison.get_samples()
        self.assertIn(reverse('clonotypes.views.detail', args=[
                      self.comparison.id]), response.content)

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

    def test_sample_compare_form_uses_a_template_tag(self):
        from django.template import Template, Context
        t = Template('{% load comparison_tags %}{% sample_compare_tag sample_compare_form %}')
        c = Context({'sample_compare_form': None})
        self.assertIn('<form action=', t.render(c))

    def test_compare_view_uses_a_template_tag(self):
        from django.template import Template, Context
        t = Template(
            '{% load comparison_tags %}{% comparison_tag comparison %}')
        c = Context({'comparison': self.comparison})
        response = self.client.get(reverse(
            'cf_comparisons.views.compare', args=[self.comparison.id]))
        self.assertTemplateUsed(response.content,
                                t.render(c))

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
        self.assertIn('<input type="submit"', response.content)

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
        clonofilters = self.comparison.clonofilters_all()
        samples = [clonofilter.sample for clonofilter in clonofilters]
        response = self.client.get(reverse('cf_comparisons.views.compare',
                                           args=[self.comparison.id]))
        self.assertIn(str(samples[0]), response.content)

    def test_filter_forms_uses_a_template_tag(self):
        from django.template import Template, Context
        t = Template(
            '{% load comparison_tags %}{% filter_forms_tag filter_forms %}')
        c = Context({'filter_forms': self.comparison.filter_forms_list()})
        self.assertIn('<form action=', t.render(c))


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
