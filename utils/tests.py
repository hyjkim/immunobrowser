from django.test import TestCase
from utils.text_manipulation import convert

class TextManipulationTest(TestCase):
  def test_convert_camel_case(self):
    self.assertEquals(convert('aminoAcid'), 'amino_acid')
    self.assertEquals(convert('cdr3Length'), 'cdr3_length')
    self.assertEquals(convert('d5Deletion'), 'd5_deletion')

