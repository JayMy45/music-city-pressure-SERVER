from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date_hired = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    phone_number = PhoneField(blank=True, help_text='Contact phone number')
    salary = models.FloatField()
    specialty = models.CharField(max_length=155)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
