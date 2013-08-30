from django.test import TestCase
from dashboard.templatetags.dashboard_tags import menu_tag

class DashboardMenuTagTests(TestCase):
    '''
    Tests menu tag for correct activation
    '''

    def test_tag_accepts_keywords_to_highlight_a_view(self):
        self.fail('todo')

    def test_tag_returns_array_of_dicts_that_store_view_name_and_active_status(self):
        context = menu_tag()
        for item in context['menu']:
            self.assertIsInstance(item['view'], unicode)
            self.assertIsInstance(item['name'], unicode)
            self.assertIsInstance(item['active'], bool)
