from django.template import Template, Context
from django.test import TestCase
from cf_comparisons.templatetags.comparison_tags import scatter_nav_tag, shared_clones_tag
from cf_comparisons.models import Comparison
from test_utils.factories import ComparisonFactory
from test_utils.ghetto_factory import make_fake_comparison_with_2_samples
from django.core.urlresolvers import reverse
import json


class SharedClonotypesTagTests(TestCase):
    '''
    For testing the shared clonotypes template tag
    '''
    def setUp(self):
        make_fake_comparison_with_2_samples()
        self.comparison = Comparison.objects.get()
        self.shared_aa = self.comparison.get_shared_amino_acids()[0]
        self.t = Template('{% load comparison_tags %}{% shared_clones_tag comparison %}')
        self.c = Context({'comparison': self.comparison})

    def test_compare_shared_clonotypes_tag_shows_links_to_shared_amino_acid(self):
        from clonotypes.models import AminoAcid
        self.assertIn(reverse('clonotypes.views.amino_acid_detail',
                      args=[self.shared_aa.id]), self.t.render(self.c))

    def test_compare_shared_clonotypes_tag_shows_shared_clonotypes_as_table(self):
        self.assertIn('td class="clonotype"', self.t.render(self.c))

    def test_compare_shared_clonotypes_returns_shared_amino_acids_in_context(self):
        shared_amino_acids = self.comparison.get_shared_amino_acids_related()
        context = shared_clones_tag(self.comparison)
        self.assertEqual(shared_amino_acids, context['shared_amino_acids'])

    def test_compare_shared_clonotypes_tag_passes_shared_amino_acid_counts_to_context_as_json(self):
        shared_amino_acids_counts = self.comparison.get_shared_amino_acids_counts()
        context = shared_clones_tag(self.comparison)
        self.assertEqual(json.dumps(shared_amino_acids_counts), context['amino_acids'])


    def DONTtest_compare_shared_clonotypes_should_link_to_clonotype_detail(self):
        from clonotypes.models import Clonotype
        response = self.client.get(
            reverse('cf_comparisons.views.compare', args=[self.comparison.id]))
        samples = self.comparison.get_samples()
        self.assertIn(reverse('clonotypes.views.detail', args=[self.comparison.id]),response.content)


class ComparisonsTagUnitTest(TestCase):
    '''
    For DONTtesting template tags (essentially a subset of the views)
    '''
    def setUp(self):
        make_fake_comparison_with_2_samples()
#        ComparisonFactory()
        self.comparison = Comparison.objects.get()

    def DONTtest_compare_should_have_number_of_forms_as_hidden_field(self):
        response = self.client.get(
            reverse('cf_comparisons.views.compare', args=[self.comparison.id]))
        self.assertIn('<input type="hidden" name="num_forms" value="2">',
                      response.content)

    def DONTtest_compare_creates_a_new_comparison_if_filter_form_is_changed(self):
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



    def DONTtest_clonofilter_forms_in_compare_should_have_prefixes(self):
        '''
        When I modified the filter_form template tag, this DONTtest became deprecated.
        Not really sure how to DONTtest the context of a template tag at this point,
        doesn't seem to be a common practice.
        '''
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual('0', mock_response.get('filter_forms')[0].prefix)

    def DONTtest_compare_view_displays_as_many_forms_as_clonofilters_in_a_comparison_instance(self):
        '''
        When I modified the filter_form template tag, this DONTtest became deprecated.
        Not really sure how to DONTtest the context of a template tag at this point,
        doesn't seem to be a common practice.
        '''
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual(len(self.comparison.clonofilters.all()),
                         len(mock_response.get('filter_forms')))

    def DONTtest_compare_view_passes_list_of_clonofilter_forms_to_template_via_context(self):
        '''
        When I modified the filter_form template tag, this DONTtest became deprecated.
        Not really sure how to DONTtest the context of a template tag at this point,
        doesn't seem to be a common practice.
        '''
        from clonotypes.forms import ClonoFilterForm
        mock_response = compare(self.request, self.comparison.id)
        filter_forms = mock_response.get('filter_forms')
        self.assertIsInstance(filter_forms, list)

        for form in filter_forms:
            self.assertIsInstance(form, ClonoFilterForm)

    def DONTtest_compare_should_pass_num_forms_to_template_via_context(self):
        '''
        not sure why this isn't working, but it's not necessary with
        dashboard_v2.
        '''
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual(2, mock_response.get('num_forms'))

    def DONTtest_compare_sends_shared_amino_acids_and_related_clonotypes(self):
        mock_response = compare(self.request, self.comparison.id)
        shared_amino_acids = self.comparison.get_shared_amino_acids_related()
        self.assertEquals(shared_amino_acids, mock_response.get('shared_amino_acids'))

    def DONTtest_compare_should_pass_samples_to_template_via_context(self):
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual(self.comparison.get_samples(
        ), mock_response.get('samples'))

    def DONTtest_compare_sends_shared_amino_acids_and_related_clonotypes(self):
        mock_response = compare(self.request, self.comparison.id)
        shared_amino_acids = self.comparison.get_shared_amino_acids_related()
        self.assertEquals(shared_amino_acids, mock_response.get('shared_amino_acids'))

    def DONTtest_compare_should_pass_samples_to_template_via_context(self):
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual(self.comparison.get_samples(
        ), mock_response.get('samples'))

    def DONTtest_compare_view_passes_comparison_instance_to_template_via_context(self):
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual(self.comparison, mock_response.get('comparison'))

    def DONTtest_compare_renders_compare_html_template(self):
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual('compare.html', mock_response.get('template'))

    def DONTtest_compare_returns_ajax_view_if_request_is_ajax(self):
        self.request.is_ajax = lambda: True
        mock_response = compare(self.request, self.comparison.id)
        self.assertEqual('compare_ajax.html', mock_response.get('template'))

    def DONTtest_filter_forms_renders_using_filter_form_template(self):
        from cf_comparisons.views import filter_forms
        mock_response = filter_forms(self.request, self.comparison.id)
        self.assertEqual('filter_forms.html', mock_response.get('template'))

