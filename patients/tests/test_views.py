from django.test import TestCase
from test_utils.factories import PatientFactory, render_echo, FakeRequestFactory
from django.core.urlresolvers import reverse
from patients.views import patient_summary
from mock import patch


class PatientsViewUnitTest(TestCase):
    def setUp(self):
        self.renderPatch = patch('patients.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()

    def tearDown(self):
        self.renderPatch.stop()

    def test_patient_view_uses_summary_template(self):
        patient = PatientFactory()
        mock_response = patient_summary(self.request, patient.id)
        self.assertEqual('patient_summary.html', mock_response.get('template'))

class PatientsViewIntegrationTest(TestCase):
    def setUp(self):
        self.patient = PatientFactory()

    def test_patient_view_exists(self):
        self.client.get(reverse('patients.views.patient_summary', args=[self.patient.id]))

    def test_tastypie_api_returns_json(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'patient', 'api_name': 'v1'});
        response = self.client.get(url)
        self.assertEqual('{"meta": {"limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 1}, "objects": [{"birthday": "2011-11-11", "disease": "fake disease", "gender": "M", "id": 1, "name": "test patient", "resource_uri": "/api/v1/patient/1/"}]}', response.content)
