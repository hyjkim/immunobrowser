from django.test import TestCase
from test_utils.factories import render_echo, FakeRequestFactory, PatientFactory, SampleFactory
from mock import patch
from dashboard.views import explorer, menu_json
from django.core.urlresolvers import reverse
import simplejson as json

class DashboardViewUnitTest(TestCase):
    ''' Here, we mock out the rendering stack for fast unit tests of the view'''

    def setUp(self):
        self.renderPatch = patch('dashboard.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()

    def tearDown(self):
        self.renderPatch.stop()

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

    def test_explorer_should_pass_patients_to_template_via_context(self):
        from patients.models import Patient
        PatientFactory()
        PatientFactory()

        mock_response = explorer(self.request)
        self.assertEqual(
            map(repr, Patient.objects.all()),
            map(repr, mock_response.get('patients'))
        )

    def test_explorer_should_render_explorer_template(self):
        from patients.models import Patient
        mock_response = explorer(self.request)
        self.assertEqual('explorer.html', mock_response.get('template'))


class DashboardViewIntegrationTest(TestCase):
    ''' For testing dashboard stuff that requires calling the call stack '''
    def DONTtest_explorer_url_is_valid(self):
        ''' Not tested because other tests do the same thing '''
        self.client.get(reverse('dashboard.views.explorer'))

    def test_menu_json_route_exists(self):
        reverse('dashboard.views.menu_json')

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
