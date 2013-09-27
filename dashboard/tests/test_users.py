from django.test import TestCase
from django.core.urlresolvers import reverse


class UserPrivacyTests(TestCase):
    def test_menu_displays_link_to_logout_if_user_is_logged_in(self):
        from test_utils.factories import UserFactory
        from django.core.urlresolvers import reverse
        password = 'incrediblysecurepassword'
        user = UserFactory(password=password)
        self.client.login(username=user.username, password=password)

        url = reverse('django.contrib.auth.views.logout')
        response = self.client.get(reverse('dashboard.views.home'))
        self.assertIn(url, response.content)
        self.fail('refactor')

    def test_recombination_belonging_to_only_to_a_private_clonotype_is_not_viewable(self):
        self.fail('todo')

    def test_clonotype_belonging_to_a_private_sample_is_not_viewable(self):
        self.fail('todo')

    def test_amino_acid_belonging_to_only_to_a_private_recombination_is_not_viewable(self):
        self.fail('todo')

class UserUnitTest(TestCase):
    '''
    Testing mockable portions of the views
    '''

    def setUp(self):
        self.renderPatch = patch('dashboard.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()

    def tearDown(self):
        self.renderPatch.stop()

class UserIntegrationTest(TestCase):
    '''
    For testing user interaction tests
    '''

    def test_login_page_has_link_to_create_a_new_user(self):
        response = self.client.get(reverse('django.contrib.auth.views.login'))
        self.assertIn(reverse('registration_register'), response.content)

    def test_login_page_has_link_to_login(self):
        response = self.client.get(reverse('django.contrib.auth.views.login'))
        self.assertIn(reverse('django.contrib.auth.views.login'), response.content)

    def test_login_page_exists(self):
        response = self.client.get(reverse('django.contrib.auth.views.login'))
        self.assertTrue(response.content)
