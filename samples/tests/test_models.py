from django.test import TestCase
from datetime import date
from test_utils.ghetto_factory import make_fake_patient_with_3_clonotypes
from samples.models import Sample
#from patients.models import Patient


class SampleModelTest(TestCase):
    def setUp(self):
        make_fake_patient_with_3_clonotypes()

    def test_create_samples_for_a_patient(self):
        # Try retreiving the sample from the database
        s = Sample.objects.get()
        all_samples = Sample.objects.all()
        self.assertEqual(len(all_samples), 1)

        # Check to see if the attributes have been saved

        # Make sure the sample is linked to the patient
        self.assertEqual(all_samples[0].patient, s.patient)

    def test_samples_have_a_draw_date(self):
        # Retrieve the sample from the db
        all_samples = Sample.objects.all()
        # make sure the draw dates are equal
        self.assertTrue(all_samples[0].draw_date)
