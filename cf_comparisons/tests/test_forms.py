from django.test import TestCase
from test_utils.ghetto_factory import make_fake_comparison_with_2_samples
from cf_comparisons.forms import SampleCompareForm


class ComparisonFormTest(TestCase):
    '''
    Test forms associated with generated new comparisons
    '''
    def test_compare_sample_form_displays_all_samples(self):
        '''
        Check to make sure that all samples are displayed in the sample
        compare form
        '''
        from samples.models import Sample

        make_fake_comparison_with_2_samples()
        form = SampleCompareForm()
        rendered_form = form.as_p()
        for sample in Sample.objects.all():
            self.assertIn(str(sample), rendered_form)
