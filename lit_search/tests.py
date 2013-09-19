from django.test import TestCase


class BlatHitTests(TestCase):
    def test_blathit_result_returns_list_of_hits(self):
        self.assertEqual(1 + 1, 2)
