from django.test import TestCase
from test_utils.factories import render_echo, FakeRequestFactory, PatientFactory, SampleFactory, ComparisonFactory
from mock import patch
from dashboard.views import explorer, menu_json, add_samples, dashboard_comparison, compare_v2, add_samples_v2, search
from django.core.urlresolvers import reverse
from cf_comparisons.models import Comparison
import simplejson as json
from test_utils.factories import UserFactory


class SearchUnitTest(TestCase):
    def setUp(self):
        self.renderPatch = patch('dashboard.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()

    def tearDown(self):
        self.renderPatch.stop()

    def test_searched_recombinations_and_amino_acids_are_paginated(self):
        from django.core.paginator import Page
        SampleFactory()
        self.request = FakeRequestFactory(GET={'query': 'atc cas'})
        response = search(self.request)
        self.assertIsInstance(response['recombinations'], Page)
        self.assertIsInstance(response['amino_acids'], Page)

    def test_search_passes_search_form_to_template_via_context(self):
        from dashboard.forms import SearchForm
        response = search(self.request)
        self.assertIsInstance(response['search_form'], SearchForm)

    def test_search_sends_matching_samples_to_template_via_context(self):
        from test_utils.factories import SampleFactory
        from samples.models import Sample
        SampleFactory()
        self.request = FakeRequestFactory(GET={'query': 'patient'})
        response = search(self.request)
        self.assertEqual((map(repr, Sample.objects.all())),
                map(repr, response['samples']))

    def test_search_renders_search_template(self):
        response = search(self.request)
        self.assertEqual(response['template'], "search.html")

    def test_search_has_a_valid_url(self):
        url = reverse('dashboard.views.search')
        self.assertTrue(url)

class HomeViewIntegrationTest(TestCase):
    def test_home_uri_is_root(self):
        self.assertEqual(reverse('dashboard.views.home'), '/')

class DashboardViewUnitTest(TestCase):
    ''' Here, we mock out the rendering stack for fast unit tests of the view'''

    def setUp(self):
        self.renderPatch = patch('dashboard.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()

    def tearDown(self):
        self.renderPatch.stop()

    def test_compare_v2_passes_search_form_to_template_via_context(self):
        from dashboard.forms import SearchForm
        response = compare_v2(self.request, None)
        self.assertIsInstance(response['search_form'], SearchForm)


    def test_compare_v2_passes_given_comparison_to_template(self):
        comp = ComparisonFactory()
        response = compare_v2(self.request, comp.id)
        self.assertEqual(response['comparison'], comp)

    def test_compare_v2_passes_sample_compare_form_to_view(self):
        from cf_comparisons.forms import SampleCompareForm
        response = compare_v2(self.request, None)
        self.assertIsInstance(
                response['sample_compare_form'],
                SampleCompareForm
                )

    def test_compare_v2_view_renders_dashbaord_v2_template(self):
        response = compare_v2(self.request, None)
        self.assertEqual(response['template'], "compare_v2.html")

    def test_add_samples_takes_in_string_of_comma_delimited_sample_ids_via_post_and_returns_a_comparison_id(self):
        self.request.POST['sample_ids'] = "[1,2,3]"
        response = add_samples(self.request)
        self.assertEqual('1', response.content)

    def test_menu_json_returns_http_response_json(self):
        from django.http import HttpResponse
        response = menu_json(self.request)
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual('application/json', response['content-type'])

    def test_menu_json_should_return_json_object_containing_patient_labels(self):
        PatientFactory()
        response = menu_json(self.request)
        menu = json.loads(response.content)
        self.assertEqual('test patient', menu[0]['label'])

    def test_menu_json_reponse_should_contain_patient_id(self):
        PatientFactory()
        response = menu_json(self.request)
        menu = json.loads(response.content)
        self.assertEqual('patient_1', menu[0]['id'])

    def test_menu_json_response_should_contain_label_for_each_child(self):
        p = PatientFactory()
        s = SampleFactory(patient=p)
        s2 = SampleFactory(patient=p)
        response = menu_json(self.request)
        menu = json.loads(response.content)
        self.assertEqual(str(s), menu[0]['children'][0]['label'])
        self.assertEqual(str(s2), menu[0]['children'][1]['label'])

    def test_menu_json_response_should_contain_label_for_each_child(self):
        p = PatientFactory()
        s = SampleFactory(patient=p)
        s2 = SampleFactory(patient=p)
        response = menu_json(self.request)
        menu = json.loads(response.content)
        self.assertEqual('sample_%s' % (str(s.id)), menu[0]['children'][0]['id'])
        self.assertEqual('sample_%s' % (str(s2.id)), menu[0]['children'][1]['id'])

    def test_dashboard_should_show_all_patients_and_samples_in_hierarchical_sidebar(self):
        pass




class DashboardViewIntegrationTest(TestCase):
    ''' For testing dashboard stuff that requires calling the call stack '''
    def DONTtest_explorer_url_is_valid(self):
        ''' Not tested because other tests do the same thing '''
        self.client.get(reverse('dashboard.views.explorer'))




    def test_compare_v2_call_shared_clones_template_tag_if_comparison_is_not_none(self):
        comp = ComparisonFactory()
        url = reverse('dashboard.views.compare_v2', args=[comp.id])
        response = self.client.get(url)
        self.assertIn('<div id="shared-clones"', response.content)


    def test_remove_clonofilter_removes_a_clonofilter_from_a_comparison(self):
        comp = ComparisonFactory()
        cfs = list(comp.clonofilters.all())
        del_cf = cfs.pop()

        url = reverse('dashboard.views.remove_clonofilter')
        post_data = {'comparison': comp.id, 'clonofilter': del_cf.id}
        response = self.client.post(url, data=post_data)
        self.assertNotEqual(comp.id, response.content)
        new_comp = Comparison.objects.get(id=response.content)
        self.assertEqual([cf.id for cf in cfs], [cf.id for cf in new_comp.clonofilters.all()])

    def test_add_samples_v2_adds_new_samples_to_existing_in_comparison_and_returns_new_comp_id(self):
        from test_utils.factories import SampleFactory
        comp = ComparisonFactory()
        sample = SampleFactory()

        old_cfs = comp.clonofilters.all()
        old_sample_set = set([cf.sample for cf in comp.clonofilters.all()])

        url = reverse('dashboard.views.add_samples_v2')
        post_data = {'comparison': comp.id, 'samples': [sample.id]}
        response = self.client.post(url,
                                    data=post_data)

        new_comp_id = response.content
        new_comp = Comparison.objects.get(id=new_comp_id)
        new_sample_set = set([cf.sample for cf in new_comp.clonofilters.all()])
        self.assertTrue(sample in new_sample_set)
        self.assertTrue(old_sample_set.issubset(new_sample_set))

    def test_compare_v2_shows_sample_select_template_tag(self):
        url = reverse('dashboard.views.compare_v2')
        response = self.client.get(url)
        ComparisonFactory()
        comp = Comparison.objects.get()
        self.assertIn('<select multiple="multiple" id="id_samples"', response.content)

    def test_comparison_view_renders_comparison_template(self):
        from test_utils.ghetto_factory import make_fake_comparison_with_2_samples
        from cf_comparisons.models import Comparison
        make_fake_comparison_with_2_samples()
        comparison = Comparison.objects.get()
        response = self.client.get(reverse('dashboard.views.dashboard_comparison', args=[comparison.id]))
        self.assertTemplateUsed(response, 'dashboard_comparison.html')

    def test_explorer_should_pass_patients_to_template_via_context(self):
        from patients.models import Patient
        PatientFactory()
        PatientFactory()

        mock_response = self.client.get(reverse('dashboard.views.explorer'))
        self.assertEqual(
            map(repr, Patient.objects.all()),
            map(repr, mock_response.context['patients'])
        )

    def test_explorer_should_render_explorer_template(self):
        response = self.client.get(reverse('dashboard.views.explorer'))
        self.assertTemplateUsed(response, 'explorer.html')

    def test_add_samples_route_exists(self):
        url = reverse('dashboard.views.add_samples')
        self.assertEqual('/dashboard/add_samples', url)

    def test_menu_json_route_exists(self):
        url = reverse('dashboard.views.menu_json')
        self.assertEqual('/dashboard/menu.json', url)

    def test_explorer_should_display_a_checkbox_by_each_patient_and_sample(self):
        patients = [PatientFactory() for x in range(2)]
        [SampleFactory(patient=p) for p in patients]
        response = self.client.get(reverse('dashboard.views.explorer'))

        for patient in patients:
            self.assertIn('<input type="checkbox" id="patient_%s"' %(patient.id), response.content)
            for sample in patient.sample_set.all():
                self.assertIn('<input type="checkbox" id="sample_%s"' %(sample.id), response.content)

    def test_explorer_should_display_all_patients_and_samples_with_links(self):
        patients = [PatientFactory() for x in range(2)]
        [SampleFactory(patient=p) for p in patients]

        response = self.client.get(reverse('dashboard.views.explorer'))

        for patient in patients:
            self.assertIn(str(patient), response.content)
            self.assertIn(reverse('patients.views.patient_summary',
                          args=[patient.id]), response.content)
            for sample in patient.sample_set.all():
                self.assertIn(str(sample), response.content)
                self.assertIn(reverse('samples.views.summary',
                              args=[sample.id]), response.content)


class UserUnitTest(TestCase):
    '''
    Testing mockable portions of the views
    '''

    def setUp(self):
        self.renderPatch = patch('dashboard.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()

    def tearDown(self):
        self.renderPatch.stop()

class UserIntegrationTest(TestCase):
    '''
    For testing user interaction tests
    '''

    def test_compare_v2_does_not_display_link_to_login_if_user_is_logged_in(self):
        password = 'incrediblysecurepassword'
        user = UserFactory(password=password)
        self.client.login(username=user.username, password=password)

        response = self.client.get(reverse('dashboard.views.compare_v2'))
        self.assertNotIn(reverse('django.contrib.auth.views.login'), response.content)


    def test_compare_v2_has_link_to_create_a_new_user(self):
        response = self.client.get(reverse('django.contrib.auth.views.login'))
        self.assertIn(reverse('registration_register'), response.content)

    def test_compare_v2_has_link_to_login(self):
        response = self.client.get(reverse('django.contrib.auth.views.login'))
        self.assertIn(reverse('django.contrib.auth.views.login'), response.content)

    def test_login_page_exists(self):
        response = self.client.get(reverse('django.contrib.auth.views.login'))
        self.assertTrue(response.content)
