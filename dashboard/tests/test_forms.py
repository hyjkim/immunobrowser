from django.test import TestCase
from dashboard.forms import SearchForm

class DashboardFormTest(TestCase):
    '''
    Tests forms associated wtih dashboard
    '''
    def test_search_form_contains_query_field(self):
        from django.forms import CharField
        self.assertIsInstance(SearchForm().fields['query'], CharField)
