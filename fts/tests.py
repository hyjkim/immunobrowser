from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver

# Setting up the functional tests
#def setUp(self):
#  self.browser = webdriver.Firefox()
#  self.browser.implicitly_wait(3)
#def tearDown(self):
#  self.browser.quit()

class PatientsTest(LiveServerTestCase):

  def test_can_create_new_patient_via_admin_site(self):
    self.fail('TODO')
    # Bjork 

class SamplesTest(LiveServerTestCase):
  def test_can_create_new_sample_via_admin_site(self):
    self.fail('TODO')

class RepertoiresTest(LiveServerTestCase):
  def test_can_create_new_repertoire_via_admin_site(self):
    self.fail('TODO')
