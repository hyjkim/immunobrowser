from django.test import TestCase
from django.core.urlresolvers import reverse
from test_utils.ghetto_factory import make_fake_patient
from clonotypes.forms import ClonoFilterForm
from samples.models import Sample
from django import forms
from immuno.helpers import *


class ClonotypeFormTest(TestCase):

    def setUp(self):
        make_fake_patient()
        self.s = Sample.objects.get()

    def test_form_renders_sample_id(self):
        form = ClonoFilterForm(initial={'sample': self.s})
        self.assertIn(str(self.s.id), form.as_p())
#        self.assertEqual(form.cleaned_data['sample_id'], s.id)

    def test_form_renders_min_copy_as_int_fields(self):
        form = ClonoFilterForm(initial={'sample':self.s})
        self.assertIsInstance(
            form.fields['min_copy'], forms.fields.IntegerField)

    def DONTtest_form_renders_max_copy_as_int_fields(self):
        form = FilterForm()
        self.assertIsInstance(
            form.fields['max_copy'], forms.fields.IntegerField)


    def DONTtest_form_renders_min_max_length_as_int_fields(self):
        form = FilterForm()
        self.assertIsInstance(
            form.fields['min_cdr3_length'], forms.fields.IntegerField)
        self.assertIsInstance(
            form.fields['max_cdr3_length'], forms.fields.IntegerField)

    def DONTtest_form_renders_filter_choices_as_checkboxes(self):
        form = FilterForm()
        self.assertEquals(form.fields['filters'].choices, [
            ("Productive", "Productive"),
            ("Out of frame", "Out of frame"),
            ("Has Stop", "Has Stop")
        ])
        self.assertIn('input type="checkbox" name="filters"', form.as_p())

    def DONTtest_summary_page_shows_productivity_choices_using_form(self):
        make_fake_patient()
        fake_sample = Sample.objects.get()

        response = self.client.get(reverse('samples.views.summary',
                                   args=[fake_sample.id]))
        self.assertTrue(isinstance(response.context['form'], FilterForm))