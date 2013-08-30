from django.test import TestCase
from dashboard.templatetags.dashboard_tags import menu_tag
from django.template import Template, Context

class DashboardMenuTagTests(TestCase):
    '''
    Tests menu tag for correct activation
    '''

    def test_menu_tag_with_valid_view_argument_the_view_is_active(self):
        t = Template("{% load dashboard_tags %}{% menu_tag 'dashboard.views.dashboard_v2'%}")
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
        view = 'dashboard.views.dashboard_v2'
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
