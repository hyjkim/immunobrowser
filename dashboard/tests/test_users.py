from django.test import TestCase


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
