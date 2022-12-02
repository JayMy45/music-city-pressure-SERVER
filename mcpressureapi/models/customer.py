from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneField(blank=True, help_text='Contact phone number')
    address = models.CharField(max_length=200)