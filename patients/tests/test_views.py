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
    def test_patient_view_exists(self):
        patient = PatientFactory()
        self.client.get(reverse('patients.views.patient_summary', args=[patient.id]))
