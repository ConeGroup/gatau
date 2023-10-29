from django.db import models
from django.contrib.auth.models import User
from book.models import Book

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    rating = models.FloatField()
    book_review_desc = models.TextField()
    is_recommended = models.BooleanField()