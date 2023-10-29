from django.test import TestCase, Client

class mainTest(TestCase):
    # Apakah html userprofile ada
    def test_userprofile_url_is_exist(self):
        response = Client().get('/userprofile/')
        self.assertEqual(response.status_code, 200)


