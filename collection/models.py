
# Create your models here.
from django.db import models
from book.models import Book
from django.contrib.auth.models import User

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book)