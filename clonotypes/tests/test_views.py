from django.test import TestCase
#from patients.models import Patient
from samples.models import Sample
from clonotypes.models import Clonotype
from django.core.urlresolvers import reverse
from test_utils.ghetto_factory import make_fake_patient, make_fake_patient_with_3_clonotypes
from mock import MagicMock, patch
from clonotypes.views import all
from test_utils.factories import render_echo, FakeRequestFactory


class ClonotypesMockedViewTest(TestCase):
    ''' ClonotypesMockedViewTest mocks out the Django call stack for faster unit tests.
    This is useful for testing the view and making sure objects exist in the context and that
    the correct templates are being used. This also increases the speed of the unittesting

    '''

    def setUp(self):
        self.renderPatch = patch('clonotypes.views.render', render_echo)
        self.renderPatch.start()

    def tearDown(self):
        self.renderPatch.stop()

    def test_clonotypes_are_passed_to_template_mocked(self):
        make_fake_patient_with_3_clonotypes()
        fake_sample = Sample.objects.get()
        request = FakeRequestFactory()
        context = {}

        render = all(request, fake_sample.id)
        self.assertEquals(render['template'], 'all.html')

    def test_mock_all(self):
# These should be replaced with mocks
        make_fake_patient_with_3_clonotypes()
        fake_sample = Sample.objects.get()

# Make a fake request
        request = FakeRequestFactory()
# Patch out the render_to_response method to return what was passed
#        patch('clonotypes.views.all.render', render_echo).start()
#        patch('django.shortcuts.render', render_echo).start()
        render = all(request, fake_sample.id)
        self.fail()


class ClonotypesViewTest(TestCase):

    def test_clonotypes_paginated_view_passes_paginated_clonotypes_to_template(self):
        self.assertEqual(0, len(Sample.objects.all()))
        make_fake_patient_with_3_clonotypes()
        fake_sample = Sample.objects.get()
        fake_clonotypes = Clonotype.objects.filter(sample=fake_sample)
        response = self.client.get(
            reverse('clonotypes.views.pagination', args=[fake_sample.id]))
        clonotypes_in_context = response.context['clonotypes']
# Comparing querysets may be less messy by monkeypatching TestCase with
# assertEqualQueryset. Check http://djangosnippets.org/snippets/2013/
        pk = lambda o: o.pk
        self.assertEqual(list(sorted(fake_clonotypes, key=pk)),
                         list(sorted(clonotypes_in_context, key=pk)))

    def test_clonotypes_paginated_view_renders_list_template(self):
        make_fake_patient()
        fake_sample = Sample.objects.get()
        response = self.client.get(
            reverse('clonotypes.views.pagination', args=[fake_sample.id]))
        self.assertTemplateUsed(response, 'list.html')

    def test_clonotypes_views_all_renders_all_template(self):
        make_fake_patient()
        fake_sample = Sample.objects.get()
        response = self.client.get(
            reverse('clonotypes.views.all', args=[fake_sample.id]))
        self.assertTemplateUsed(response, 'all.html')

    def test_clonotypes_all_view_shows_summary_template(self):
        make_fake_patient()
        fake_sample = Sample.objects.get()
        response = self.client.get(
            reverse('clonotypes.views.all', args=[fake_sample.id]))

        self.assertIn('test patient', response.content)

    def test_clonotypes_all_view_passes_clonotypes_to_template(self):
        self.assertEqual(0, len(Sample.objects.all()))
        make_fake_patient_with_3_clonotypes()
        fake_sample = Sample.objects.get()
        fake_clonotypes = Clonotype.objects.filter(sample=fake_sample)
        response = self.client.get(
            reverse('clonotypes.views.all', args=[fake_sample.id]))
        clonotypes_in_context = response.context['clonotypes']
# Comparing querysets may be less messy by monkeypatching TestCase with
# assertEqualQueryset. Check http://djangosnippets.org/snippets/2013/
        pk = lambda o: o.pk
        self.assertEqual(list(sorted(fake_clonotypes, key=pk)),
                         list(sorted(clonotypes_in_context, key=pk)))

    def test_clonotypes_all_view_passes_sample_to_template(self):
        make_fake_patient()
        fake_sample = Sample.objects.get()
        response = self.client.get(
            reverse('clonotypes.views.all', args=[fake_sample.id]))
        sample_in_context = response.context['sample']
        self.assertEqual(sample_in_context, fake_sample)
