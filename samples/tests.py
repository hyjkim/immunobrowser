from django.test import TestCase
from samples.models import Sample
from patients.models import Patient
import datetime
from datetime import date
from flexmock import flexmock

class SampleViewTest(TestCase):
  def test_samples_url_shows_all_samples(self):
    # make a patient
    p = Patient(name="Test Patient")
    p.save()
    # set up some samples
    sample1 = Sample(patient = p, draw_date='2011-11-11', cell_type='cd8+')
    sample1.save()
    sample2 = Sample(patient = p, draw_date='2011-11-11', cell_type='cd8-')
    sample2.save()

    # Retrieve all saved samples from the database
    all_samples = Sample.objects.all()

    # Get the samples page
    response = self.client.get('/samples/')

    # Make sure we're using the home view
    self.assertTemplateUsed(response, 'home.html')

    # Check we passed the samples to the template
    samples_in_context = response.context['samples']
    self.assertEqual(list(samples_in_context), list(all_samples))

    for sample in all_samples:
      self.assertIn(unicode(sample), response.content)

    self.fail('TODO')

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

#  @mock.patch('datetime.date', FakeDate)
  def test_can_calculate_and_return_age(self):
#    from datetime import date
#    FakeDate.today = classmethod(lambda cls: date(2012, 1, 2))
    self.fail('TODO')
    mock = flexmock()
    mock.should_receive("datetime.date.today()").and_return("date(2012,1,2)").once

    self.assertEqual(date(2012,1,2), date.today())
    # Set birthday to last year
    p = Patient(birthday='2011-1-1')
    p.save()

    self.assertEquals(p.age, 1)


