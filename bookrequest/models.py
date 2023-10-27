from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BookReq(models.Model):
    title = models.CharField(null=True, blank=True, max_length=125)
    author = models.CharField(null=True, blank=True, max_length=125)
    year = models.IntegerField(null=True, blank=True)
    publisher = models.CharField(null=True, blank=True, max_length=125)
    initial_review = models.TextField(null=True, blank=True)
    image_s = models.CharField(null=True, blank=True, max_length=125)
    image_m = models.CharField(null=True, blank=True, max_length=125)
    image_l = models.CharField(null=True, blank=True, max_length=125)
    user = models.ForeignKey(User, on_delete=models.CASCADE)