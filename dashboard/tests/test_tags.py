from django.test import TestCase
from dashboard.templatetags.dashboard_tags import menu_tag
from django.template import Template, Context
from dashboard.forms import SearchForm

class DashboardMenuTagTests(TestCase):
    '''
    Tests menu tag for correct activation
    '''

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

    def test_menu_tag_should_display_search_query_when_passed_a_search_form(self):
        form_data = {'query': 'test123'}
        search_form = SearchForm(data=form_data)
        t = Template("{% load dashboard_tags %}{% menu_tag search_form %}")
        c = Context({'search_form': search_form})

        self.assertIn('test123', t.render(c))

    def test_menu_tag_send_search_form_to_context(self):
        context = menu_tag()
        self.assertIsInstance(context['search_form'], SearchForm)

    def test_menu_tag_with_valid_view_argument_the_view_is_active(self):
        t = Template("{% load dashboard_tags %}{% menu_tag 'cf_comparisons.views.compare_v3'%}")
        c = Context({})
        self.assertIn('active', t.render(c))

    def test_menu_tag_with_no_active_argument_has_no_active_classes(self):
        t = Template('{% load dashboard_tags %}{% menu_tag %}')
        c = Context({})
        self.assertNotIn('active', t.render(c))

    def test_menu_tag_renders_nav(self):
        t = Template('{% load dashboard_tags %}{% menu_tag %}')
        c = Context({})
        self.assertIn('<nav', t.render(c))

    def test_menu_tag_accepts_keywords_to_highlight_a_view(self):
        view = 'dashboard.views.compare_v2'
        context = menu_tag(view)
        for item in context['menu']:
            if item['view'] == view:
                self.assertTrue(item['active'])

    def test_menu_tag_returns_array_of_dicts_that_store_view_name_and_active_status(self):
        context = menu_tag()
        for item in context['menu']:
            self.assertIsInstance(item['view'], str)
            self.assertIsInstance(item['name'], str)
            self.assertIsInstance(item['active'], bool)
