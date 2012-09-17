from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class SamplesTest(LiveServerTestCase):
  fixtures = ['admin_user.json', 'patients.json']

  # Setting up the functional tests
  def setUp(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)
  def tearDown(self):
    self.browser.quit()

  def test_view_all_samples_from_sample_site(self):
    self.browser.get(self.live_server_url + '/samples/')

    self.fail('TODO')
  
  def test_can_create_new_sample_via_admin_site(self):
    # Bob wants to add a sample to an existing patient

    # He opens his web browser and navigates to the admin page
    self.browser.get(self.live_server_url + '/admin/')

    # He logs in with his username and credentials
    body = self.browser.find_element_by_tag_name('body')
    self.assertIn('Django administration', body.text)

    # He logs in with his username and password and hits return
    username_field = self.browser.find_element_by_name('username')
    username_field.send_keys('hyjkim')

    password_field = self.browser.find_element_by_name('password')
    password_field.send_keys('adm1n')
    password_field.send_keys(Keys.RETURN)

    # He now sees a couple of hyperlink that says "Patients"
    patients_links = self.browser.find_elements_by_link_text('Patients')
    self.assertEquals(len(patients_links), 2)

    # The second link looks more specific so he clicks it
    patients_links[1].click()

    # He checks to see that a patient named "Jim Harbaugh" exists
    new_patient_links = self.browser.find_elements_by_link_text("Jim Harbaugh")
    self.assertEquals(len(new_patient_links), 1)

    # He then returns to the main admin site and sees the "Samples" link
    self.browser.find_element_by_link_text('Home').click()

    # He then looks for  hyperlinks that says "Samples"
    samples_links = self.browser.find_elements_by_link_text('Samples')
    self.assertTrue(len(samples_links) > 0)

    # He then clicks the second 'Samples' link
    samples_links[1].click()

    # He looks for the 'Add sample' button and clicks it
    new_patient_link = self.browser.find_element_by_link_text('Add sample')
    new_patient_link.click()

    # He selects 'Jim Harbaugh' from the drop down menu
    patients = self.browser.find_element_by_id('id_patient')
    for option in patients.find_elements_by_tag_name('option'):
      if option.text == "Jim Harbaugh":
        option.click()

    # He types the date of "2011-11-11" for the blood draw date
    draw_date_field = self.browser.find_element_by_name('draw_date')
    draw_date_field.send_keys('11/11/2011')

    # Then he types in cd8+ for the cell type field
    cell_type_field = self.browser.find_element_by_name('cell_type')
    cell_type_field.send_keys('cd8+')
    cell_type_field.send_keys(Keys.RETURN)

    # He is returned to the samples page and sees "Jim Harbaugh 11/11/2011" as a clickable link
    body = self.browser.find_element_by_tag_name('body')
    self.assertIn("Jim Harbaugh 2011-11-11 cd8+", body.text)


class PatientsTest(LiveServerTestCase):
  fixtures = ['admin_user.json']

  # Setting up the functional tests
  def setUp(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)
  def tearDown(self):
    self.browser.quit()

  # Vernon would like to add a new patient that doesn't exist
  def test_can_create_new_patient_via_admin_site(self):
    # Vernon opens his web browser and navigates to the admin page
    self.browser.get(self.live_server_url + '/admin/')

    # He sees the 'Django administration' heading
    body = self.browser.find_element_by_tag_name('body')
    self.assertIn('Django administration', body.text)

    # He logs in with his username and password and hits return
    username_field = self.browser.find_element_by_name('username')
    username_field.send_keys('hyjkim')

    password_field = self.browser.find_element_by_name('password')
    password_field.send_keys('adm1n')
    password_field.send_keys(Keys.RETURN)

    # His username and password are accepted, and he is taken to
    # the Site Administration page
    body = self.browser.find_element_by_tag_name('body')
    self.assertIn('Site administration', body.text)

    # He now sees a couple of hyperlink that says "Patients"
    patients_links = self.browser.find_elements_by_link_text('Patients')
    self.assertEquals(len(patients_links), 2)

    # The second link looks more specific so he clicks it
    patients_links[1].click()

    # The link should route to 'admin/patients/patient/'
    self.assertEqual(self.browser.current_url, 'http://localhost:8081/admin/patients/patient/')

    # He is taken to the patient listing page, which shows there are no patients
    body = self.browser.find_element_by_tag_name('body')
    self.assertIn('0 patients', body.text)

    # He sees a link to add a new patient and clicks it
    new_patient_link = self.browser.find_element_by_link_text('Add patient')
    new_patient_link.click()

    # He seems some input fields for "Name", "Gender", "Disease" and "Birthday" 
    body = self.browser.find_element_by_tag_name('body')
    self.assertIn("Name", body.text)
    self.assertIn("Gender", body.text)
    self.assertIn("Disease", body.text)
    self.assertIn("Birthday", body.text)

    # He enters in various values
    name_field = self.browser.find_element_by_name('name')
    gender_field = self.browser.find_element_by_name('gender')
    disease_field = self.browser.find_element_by_name('disease')
    birthday_field = self.browser.find_element_by_name('birthday')

    name_field.send_keys('Jim Harbaugh')
    gender_field.send_keys('M')
    disease_field.send_keys('Freddy P. Soft Syndrome')
    birthday_field.send_keys('12/23/1963')

    # Then hits 'return' because he's too lazy to click save
    birthday_field.send_keys(Keys.RETURN)

    # He is returned to the "Patient's" page, where he can see
    # the new patient listed as a clickable link
    new_patient_links = self.browser.find_elements_by_link_text("Jim Harbaugh")
    self.assertEquals(len(new_patient_links), 1)

    # He clicks the link and verifies that the information he sees
    # matches the information he entered
    new_patient_links[0].click()

    name_field = self.browser.find_element_by_name('name')
    gender_field = self.browser.find_element_by_name('gender')
    disease_field = self.browser.find_element_by_name('disease')
    birthday_field = self.browser.find_element_by_name('birthday')

    self.assertEquals('Jim Harbaugh', name_field.get_attribute('value'))
    self.assertEquals('M', gender_field.get_attribute('value'))
    self.assertEquals('Freddy P. Soft Syndrome', disease_field.get_attribute('value'))
    self.assertEquals('1963-12-23', birthday_field.get_attribute('value'))

    # Satisfied he has a beer


class RepertoiresTest(LiveServerTestCase):
  def DONTtest_can_create_new_repertoire_via_admin_site(self):
    self.fail('TODO')
