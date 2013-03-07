def assertRedirectsNoFollow(self, response, expected_url):
    self.assertEqual(response._headers['location'], ('Location', settings.TESTSERVER + expected_url))
    self.assertEqual(response.status_code, 302)
