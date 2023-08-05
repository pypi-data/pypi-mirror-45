from django import test


class TestDjangoCsrfProtectFormForForm(test.TestCase):
    def setUp(self):
        self.client = test.Client(enforce_csrf_checks=True)

    def post(self, url, data):
        return self.client.post(url, data)

    def test_csrf_default(self):
        res = self.post('/csrf_default/', {'hello': 'world'})
        self.assertEqual(res.status_code, 403)

    def test_csrf_exempt(self):
        res = self.post('/csrf_exempt/', {'hello': 'world'})
        self.assertEqual(res.status_code, 200)

    def test_csrf_protect(self):
        res = self.post('/csrf_protect/', {'hello': 'world'})
        self.assertEqual(res.status_code, 403)

    def test_csrf_protect_form(self):
        res = self.post('/csrf_protect_form/', {'hello': 'world'})
        self.assertEqual(res.status_code, 403)


class TestDjangoCsrfProtectFormForJson(TestDjangoCsrfProtectFormForForm):
    def post(self, url, data):
        return self.client.post(url, data, content_type='application/json')

    def test_csrf_protect_form(self):
        res = self.post('/csrf_protect_form/', {'hello': 'world'})
        self.assertEqual(res.status_code, 200)
