from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date_hired = models.DateField()
    salary = models.FloatField()
    is_Staff = models.BooleanField()