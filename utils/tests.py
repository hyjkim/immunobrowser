from django.test import TestCase
from utils.text_manipulation import convert

class TextManipulationTest(TestCase):
    def test_convert_camel_case(self):
        '''
        Test: Converts a camel cased string to a underscore delimited string
        '''
        self.assertEquals(convert('aminoAcid'), 'amino_acid')
        self.assertEquals(convert('cdr3Length'), 'cdr3_length')
        self.assertEquals(convert('d5Deletion'), 'd5_deletion')


class UtilsTests(TestCase):
    def test_currentUrl_returns_url_of_request(self):
        from test_utils.factories import FakeRequestFactory
        from utils.utils import get_current_path
        fake_request = FakeRequestFactory()
        self.assertEqual('', get_current_path(request))



