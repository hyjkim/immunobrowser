from django.test import TestCase
from test_utils.factories import render_echo, FakeRequestFactory, PatientFactory, SampleFactory, ComparisonFactory
from mock import patch
from dashboard.views import search
from django.core.urlresolvers import reverse
from cf_comparisons.models import Comparison
import simplejson as json
from test_utils.factories import UserFactory


class SearchUnitTest(TestCase):
    def setUp(self):
        self.renderPatch = patch('dashboard.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()

    def tearDown(self):
        self.renderPatch.stop()

    def test_searched_recombinations_and_amino_acids_are_paginated(self):
        from django.core.paginator import Page
        SampleFactory()
        self.request = FakeRequestFactory(GET={'query': 'atc cas'})
        response = search(self.request)
        self.assertIsInstance(response['recombinations'], Page)
        self.assertIsInstance(response['amino_acids'], Page)

    def test_search_passes_search_form_to_template_via_context(self):
        from dashboard.forms import SearchForm
        response = search(self.request)
        self.assertIsInstance(response['search_form'], SearchForm)

    def test_search_sends_matching_samples_to_template_via_context(self):
        from test_utils.factories import SampleFactory
        from samples.models import Sample
        SampleFactory()
        self.request = FakeRequestFactory(GET={'query': 'patient'})
        response = search(self.request)
        self.assertEqual((map(repr, Sample.objects.all())),
                map(repr, response['samples']))

    def test_search_renders_search_template(self):
        response = search(self.request)
        self.assertEqual(response['template'], "search.html")

    def test_search_has_a_valid_url(self):
        url = reverse('dashboard.views.search')
        self.assertTrue(url)

class HomeViewIntegrationTest(TestCase):
    def test_home_uri_is_root(self):
        self.assertEqual(reverse('dashboard.views.home'), '/')

class DashboardViewUnitTest(TestCase):
    ''' Here, we mock out the rendering stack for fast unit tests of the view'''

    def setUp(self):
        self.renderPatch = patch('dashboard.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()

    def tearDown(self):
        self.renderPatch.stop()


class DashboardViewIntegrationTest(TestCase):
    ''' For testing dashboard stuff that requires calling the call stack '''
    pass
