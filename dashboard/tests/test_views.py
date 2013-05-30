from django.test import TestCase
from test_utils.factories import render_echo, FakeRequestFactory, PatientFactory, SampleFactory
from mock import patch
from dashboard.views import explorer, menu_json
from django.core.urlresolvers import reverse


class DashboardViewUnitTest(TestCase):
    ''' Here, we mock out the rendering stack for fast unit tests of the view'''

    def setUp(self):
        self.renderPatch = patch('dashboard.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()

    def tearDown(self):
        self.renderPatch.stop()

    def test_menu_json_should_return_json_object_containing_all_patients_and_samples(self):
        response = menu_json(self.request)
        self.assertEqual('{"patient1": {"sample1": "sample1", "sample2": "sample2"}}', response.content)


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
