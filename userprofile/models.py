from django.db import models
from django.contrib.auth.models import User 
from home.forms import RegisterForm

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)