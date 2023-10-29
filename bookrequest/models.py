from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

# Create your models here.

class BookReq(models.Model):
    title = models.CharField(default="Judul Kosong", max_length=50)
    author = models.CharField(default="Anonimus", max_length=50)
    isbn = models.CharField(default=1000000000, max_length=13, validators=[MinLengthValidator(10)])
    year = models.CharField(default=1966, max_length=4, validators=[MinLengthValidator(4)])
    publisher = models.CharField(default="Penerbit Tidak Diketahui", max_length=50)
    initial_review = models.TextField(null=True, blank=True, max_length=400)
    image_s = models.CharField(null=True, blank=True, max_length=125)
    image_m = models.CharField(null=True, blank=True, max_length=125)
    image_l = models.CharField(null=True, blank=True, max_length=125)
    user = models.ForeignKey(User, on_delete=models.CASCADE)