
from django.test import TestCase, Client

class mainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('/reviews/')
        self.assertEqual(response.status_code, 200)

    def test_review_page_url_is_exist(self):
        response = Client().get('/reviews/review-page/')
        self.assertEqual(response.status_code, 200)

    def test_book_details_url_is_exist(self):
        response = Client().get('/reviews/book-details/1')
        self.assertEqual(response.status_code, 200)

    def test_main_using_review_page_template(self):
        response = Client().get('/reviews/review-page/')
        self.assertTemplateUsed(response, 'review_page.html')

    def test_main_using_review_template(self):
        response = Client().get('/reviews/')
        self.assertTemplateUsed(response, 'main.html')

    def test_main_using_book_detail_template(self):
        response = Client().get('/reviews/book-details/1')
        self.assertTemplateUsed(response, 'book_details.html')


