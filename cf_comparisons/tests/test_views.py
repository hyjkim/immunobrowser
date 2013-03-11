from django.test import TestCase
from test_utils.factories import render_echo, FakeRequestFactory
from mock import patch
from test_utils.ghetto_factory import make_fake_patient_with_3_clonotypes
#from cf_comparisons.views import compare


class ComparisonsViewUnitTest(TestCase):
    '''
    Unit tests of the views patch out the render stack. For
    integration tests, write tests in ComparisonsViewIntegrationTest
    '''
    def setUp(self):
        self.renderPatch = patch('clonotypes.views.render', render_echo)
        self.renderPatch.start()
        self.request = FakeRequestFactory()
        make_fake_patient_with_3_clonotypes()

    def tearDown(self):
        self.renderPatch.stop()

    def test_compare_view_passes_list_of_clonofilters_to_template(self):
        self.fail('todo')


class ComparisonsViewIntegrationTest(TestCase):
    '''
    For integration tests that require calling the entire django
    stack. Use only when necessary
    '''
    pass
