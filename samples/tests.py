from django.test import TestCase
from samples.models import Sample
from patients.models import Patient
import datetime

class SampleModelTest(TestCase):
  def test_create_samples_for_a_patient(self):
    # Start by creating a new patient
    p = Patient()
    # and saving it to the db
    p.save()

    # Now create a Sample Object
    s = Sample()

    # Link the sample to the Patient
    s.patient = p

    # Save the sample to the database
    s.save()

    # Try retreiving the sample from the database
    all_samples = Sample.objects.all()
    self.assertEqual(len(all_samples),1)

    # Check to see if the attributes have been saved

    # Make sure the sample is linked to the patient
    self.assertEqual(all_samples[0].patient, s.patient)

  def test_samples_have_a_draw_date(self):
    # Create a new sample and patient with a draw date
    p = Patient()
    p.save()
    s = Sample()
    s.patient = p
    s.draw_date = "2011-11-11"
    # Save the sample to the database
    s.save()

    # Retrieve the sample from the db
    all_samples = Sample.objects.all()

    # Make sure it's the only one
    self.assertEquals(len(all_samples), 1)

    # make sure the draw dates are equal
    self.assertTrue(all_samples[0].draw_date)

