from django.test import TestCase
from test_utils.factories import render_echo, FakeRequestFactory
from django.core.urlresolvers import reverse
from mock import patch
from test_utils.ghetto_factory import make_fake_patient_with_3_clonotypes
from cf_comparisons.models import Comparison
from samples.models import Sample
from cf_comparisons.views import compare


class ComparisonsViewUnitTest(TestCase):
    '''
    Unit tests of the views patch out the render stack. For
    integration tests, write tests in ComparisonsViewIntegrationTest
    '''
    def setUp(self):
        self.renderPatch = patch('cf_comparisons.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()
        make_fake_patient_with_3_clonotypes()

    def tearDown(self):
        self.renderPatch.stop()

    def test_compare_view_passes_list_of_clonofilter_forms_to_template_via_context(self):
        from clonotypes.forms import ClonoFilterForm
        s = Sample.objects.get()
        comparison = Comparison.default_from_samples([s])
        mock_response = compare(self.request, comparison.id)
        filter_forms = mock_response.get('filter_forms')
        self.assertIsInstance(filter_forms, list)

        for form in filter_forms:
            self.assertIsInstance(form, ClonoFilterForm)
#        self.assertEqual(set(comparison.clonofilters.all()),
#                         set(mock_response.get('clonofilters')))

    def test_compare_view_passes_as_many_forms_as_clonofilters_in_a_comparison_instance(self):
        s = Sample.objects.get()
        comparison = Comparison.default_from_samples([s])
        mock_response = compare(self.request, comparison.id)
        filter_forms = mock_response.get('filter_forms')
        self.assertEqual(len(comparison.clonofilters.all()),
                         len(mock_response.get('filter_forms')))

    def test_compare_uses_compare_html_template(self):
        s = Sample.objects.get()
        comparison = Comparison.default_from_samples([s])
        mock_response = compare(self, comparison.id)
        self.assertEqual('compare.html', mock_response.get('template'))


class ComparisonsViewIntegrationTest(TestCase):
    '''
    For integration tests that require calling the entire django
    stack. Use only when necessary
    '''
    def test_compare_view_shows_filters_for_all_clonofilters(self):
        from patients.models import Patient
        from clonotypes.models import ClonoFilter
        make_fake_patient_with_3_clonotypes()
        p = Patient.objects.get()
        s1 = Sample.objects.get()
        s2 = Sample(patient=p, cell_type="party like it's", draw_date="1999-12-31")
        s2.save()
#        cf_1 = ClonoFilter(sample=s1)
#        cf_2 = ClonoFilter(sample=s2)
        comparison = Comparison.default_from_samples([s1, s2])

        response = self.client.get(reverse('cf_comparisons.views.compare',
                                           args=[comparison.id])
                                  )

        self.assertIn(str(s1), response.content)
#        self.assertIn(str(s2), response.content)

