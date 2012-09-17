from django.test import TestCase
from django.utils import timezone
import datetime
from patients.models import Patient


class PatientModelTest(TestCase):
  def test_patient_has_gender(self):
    # first check that db is empty
    all_patients_in_db = Patient.objects.all()
    self.assertEquals(len(all_patients_in_db), 0)

    # can create a patient that is male
    man = Patient()
    man.gender = 'M'
    man.save()

    # check db to see if patient exists
    men_in_db = Patient.objects.filter(gender='M')
    self.assertEquals(len(men_in_db), 1)
    

    # can create a patient that is female
    woman = Patient()
    woman.gender = 'F'
    woman.save()

    women_in_db = Patient.objects.filter(gender='F')
    self.assertEquals(len(women_in_db), 1)

    # can create a patient with unknown gender
    person = Patient()
    person.save()
    androgynous_people_in_db = Patient.objects.filter(gender='')
    self.assertEquals(len(androgynous_people_in_db), 1)

  def test_patient_has_name(self):
    # first check that db is empty
    all_patients_in_db = Patient.objects.all()
    self.assertEquals(len(all_patients_in_db), 0)

    # can create a patient that is male
    man = Patient()
    man.name= 'Vernon Davis'
    man.save()

    # check db to see if patient exists
    man_in_db = Patient.objects.get(name=man.name)
    self.assertEquals(man.name, man_in_db.name)

  def test_patient_has_disease(self):
    all_patients_in_db = Patient.objects.all()
    self.assertEquals(len(all_patients_in_db), 0)

    # can create a patient that is male
    man = Patient()
    man.disease = "Ankylosing Spondylitis"
    man.save()

    # check db to see if patient exists
    man_in_db = Patient.objects.get(disease=man.disease)
    self.assertEquals(man.disease, man_in_db.disease)


  def test_patient_has_birthday(self):
    all_patients_in_db = Patient.objects.all()
    self.assertEquals(len(all_patients_in_db), 0)

    # can create a patient that is male
    man = Patient()
    man.birthday = timezone.now()
    man.save()

    # check db to see if patient exists
    man_in_db = Patient.objects.get(birthday=man.birthday)
    self.assertEquals(man.birthday.date(), man_in_db.birthday)
  


  def test_can_create_a_new_patient_and_save_to_db(self):
    pass
    # Start by creating a new patient

  def test_patient_objects_are_named_after_their_name(self):
    p = Patient()
    p.name = "Lady Gaga"
    self.assertEquals(unicode(p), "Lady Gaga")
