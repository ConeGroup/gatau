import random
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from book.models import Book
from loans.models import LoansBook
from reviews.models import Review
from bookrequest.models import BookReq  
from django.utils import timezone
from userprofile.forms import EditProfileForm


class UserProfileTest(TestCase):
    def test_userprofile_url_is_exist_but(self):
        response = Client().get('/userprofile/')
        self.assertEqual(response.status_code, 302)



class ChangePasswordAjaxTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='old_password')
        self.url = reverse('userprofile:change_password_ajax')

    def test_change_password_ajax(self):
        # Log in
        self.client.login(username='testuser', password='old_password')

        # Change password
        response = self.client.post(self.url, {
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        })

        # Check response
        self.assertEqual(response.status_code, 201)

        # Check that the password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_invalid_request(self):
        # Log in
        self.client.login(username='testuser', password='old_password')

        # Send a GET request instead of POST
        response = self.client.get(self.url)

        # Check response
        self.assertEqual(response.status_code, 400)



class UserProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('userprofile')  # replace 'your_url_name' with the actual URL name
        self.book = Book.objects.create(ISBN = 'ISBN',
                    title = 'TITLE',
                    author = 'AUTHOR',
                    year = random.randint(1,4000),
                    publisher = 'PUBLISHER',
                    image_s = 'IMAGE_S',
                    image_m = 'IMAGE_M',
                    image_l = 'IMAGE_L')

    def test_show_userprofile(self):
        # Log in
        self.client.login(username='testuser', password='testpassword')

        # Create some test data
        LoansBook.objects.create(user=self.user, number_book = random.randint(1,1000000), date_loan = timezone.now(), date_return = timezone.now())
        Review.objects.create(user=self.user, book = self.book
                              ,date_added = timezone.now(),rating = random.randint(0,500) / 100,book_review_desc = 'review' ,is_recommended = bool(random.randint(0,1)))
        BookReq.objects.create(user=self.user,     title = "JUDUL KOSONG",
    author = "Anonimus",
    isbn = random.randint(1,1000000000),
    year = random.randint(1,1966),
    publisher = "Penerbit Tidak Diketahui",
    initial_review = "Penerbit Tidak Diketahui",
    image_s = "IMAGE_S",
    image_m = "IMAGE_M",
    image_l = "IMAGE_L",  )

        # Make the request
        response = self.client.get(self.url)

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['CountLoansBook'], 1)
        self.assertEqual(response.context['CountReviewBook'], 1)
        self.assertEqual(response.context['CountRequestBook'], 1)




class EditProfileAjaxTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('userprofile:edit_profile_ajax')  # replace 'your_url_name' with the actual URL name

    def test_edit_profile_ajax(self):
        # Log in
        self.client.login(username='testuser', password='testpassword')

        # Make the request
        response = self.client.post(self.url, {
            'username': 'newusername',
            'email': 'example@example.com'
        })

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Profil kamu berhasil diubah!'})

        # Check that the user's profile was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')

    def test_invalid_request(self):
        # Log in
        self.client.login(username='testuser', password='testpassword')

        # Send a GET request instead of POST
        response = self.client.get(self.url)

        # Check response
        self.assertEqual(response.status_code, 200)  # This might be different depending on your view



