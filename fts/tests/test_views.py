from django.test import TestCase
from django.core.urlresolvers import reverse


class ftsViewIntegrationTest(TestCase):
    def test_fts_qunit_view_renders_qunit_template(self):
        '''
        Checks to make sure the route exists and that the template
        rendered is the 'qunit' template
        '''
        response = self.client.get(reverse('fts.views.qunit'))
        self.assertTemplateUsed(response, 'qunit.html')
