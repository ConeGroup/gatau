from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class LoansBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_book = models.IntegerField()
    date_loan = models.DateField(default=timezone.now)
    date_return = models.DateField()
