from django.test import TestCase
#from patients.models import Patient
from samples.models import Sample
from clonotypes.models import Clonotype
from django.core.urlresolvers import reverse
from test_utils.ghetto_factory import make_fake_patient, make_fake_patient_with_3_clonotypes
from mock import MagicMock, patch
from clonotypes.views import all, detail
from test_utils.factories import render_echo, FakeRequestFactory


class ClonotypesMockedViewTest(TestCase):
    ''' ClonotypesMockedViewTest mocks out the Django call stack for faster
    unit tests. This is useful for testing the view and making sure objects
    exist in the context and that the correct templates are being used.
    This also increases the speed of the unittesting
    '''

    def setUp(self):
        self.renderPatch = patch('clonotypes.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()
        make_fake_patient_with_3_clonotypes()

    def tearDown(self):
        self.renderPatch.stop()

    def test_clonotypes_all_view_returns_paginator_object(self):
        fake_sample = Sample.objects.get()
        mock_response = all(self.request, fake_sample.id)
        self.assertEqual('Page',
                         mock_response.get('clonotypes').__class__.__name__)

    def test_clonotypes_all_view_returns_last_page_if_EmptyPage_is_thrown(self):
        from django.core.paginator import Paginator
        fake_request = FakeRequestFactory(GET={'page': 99999})
        fake_sample = Sample.objects.get()
        clonotypes = Clonotype.objects.filter(sample=fake_sample)
        paginator = Paginator(clonotypes, 2)
        mock_response = all(fake_request, fake_sample.id)
        self.assertQuerysetEqual(paginator.page(2).object_list,
                                 map(repr,
                                     mock_response.get(
                                         'clonotypes').object_list),
                                 ordered=False)

    def test_clonotypes_all_view_returns_first_page_if_PageNotAnInteger_is_thrown(self):
        from django.core.paginator import Paginator
        fake_request = FakeRequestFactory(GET={'page': 'notAnInt'})
        fake_sample = Sample.objects.get()
        clonotypes = Clonotype.objects.filter(sample=fake_sample)
        paginator = Paginator(clonotypes, 2)
        mock_response = all(fake_request, fake_sample.id)
        self.assertQuerysetEqual(paginator.page(1).object_list,
                                 map(repr,
                                     mock_response.get(
                                         'clonotypes').object_list),
                                 ordered=False)

    def test_clonotypes_all_view_calls_paginator_on_clonotypes(self):
        # Patch with a mock and then track the calls on the mock
        fake_sample = Sample.objects.get()
        mock = MagicMock()
        with patch('clonotypes.views.Paginator', return_value=mock):
            all(self.request, fake_sample.id)
            mock.page.assert_called_with(None)

    def test_clonotypes_all_view_uses_all_template(self):
        fake_sample = Sample.objects.get()
        mock_response = all(self.request, fake_sample.id)
        self.assertEqual(mock_response.get('template'), 'all.html')

    def test_clonotypes_all_view_passes_clonotypes_to_template(self):
        fake_sample = Sample.objects.get()
        fake_clonotypes = Clonotype.objects.filter(sample=fake_sample)

        mock_response = all(self.request, fake_sample.id)
        clonotypes_in_context = mock_response.get('clonotypes')

        self.assertQuerysetEqual(fake_clonotypes,
                                 map(repr, clonotypes_in_context),
                                 ordered=False)

    def test_clonotypes_all_view_passes_sample_to_template(self):
        fake_sample = Sample.objects.get()
        mock_response = all(self.request, fake_sample.id)
        sample_in_context = mock_response.get('sample')
        self.assertEqual(sample_in_context, fake_sample)

    def test_clonotype_detail_view_returns_clonotype_in_context(self):
        clonotype = Clonotype.objects.all()[:1].get()
        mock_response = detail(self.request, clonotype.id)
        self.assertEqual(clonotype, mock_response.get('clonotype'))

    def test_detail_view_has_sample_in_context(self):
        clonotype = Clonotype.objects.all()[:1].get()
        sample = clonotype.sample
        mock_response = detail(self.request, clonotype.id)
        self.assertEqual(sample, mock_response.get('sample'))


class ClonotypesAllViewTest(TestCase):
    ''' Integration tests for all clonotypes view
    '''
    def setUp(self):
        make_fake_patient()
        self.fake_sample = Sample.objects.get()
        self.response = self.client.get(
            reverse('clonotypes.views.all', args=[self.fake_sample.id]))

    def test_clonotypes_all_view_shows_patient_name(self):
        self.assertIn('test patient', self.response.content)

    def test_clonotypes_all_view_contains_pagination_page_information(self):
        self.assertIn('Page 1 of 1', self.response.content)

    def test_all_view_has_links_to_detail_view(self):
        clonotype = Clonotype.objects.all()[:1].get()
        self.assertIn('Details', self.response.content)
        self.assertIn(reverse('clonotypes.views.detail', args=[clonotype.id]),
                      self.response.content)


class ClonotypesDetailViewTest(TestCase):
    ''' Integration tests for clonotype detail view '''
    def setUp(self):
        make_fake_patient()
        self.fake_sample = Sample.objects.get()
        self.clonotype = Clonotype.objects.all()[:1].get()
        self.response = self.client.get(
            reverse('clonotypes.views.detail', args=[self.clonotype.id]))

    def test_detail_view_lists_all_info(self):
        self.assertIn('nucleotide', self.response.content)

    def test_detail_view_shows_sample_name(self):
        self.assertIn(str(self.fake_sample), self.response.content)

    def test_detail_view_uses_clonotype_template_tag(self):
        from django.template import Template, Context
        t = Template('{% load clonotype_tags %}{% clonotype_tag clonotype %}')
        c = Context({'clonotype': self.clonotype})
        t.render(c)
        self.assertEqual(c['clonotype'], self.clonotype)
        pass
