from django.db import models
from phone_field import PhoneField
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200)
    image = models.CharField(max_length=500)
    address = models.CharField(max_length=200)
    date_hired = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    phone_number = PhoneField(blank=True, help_text='Contact phone number')
    salary = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    specialty = models.ManyToManyField('Specialty', blank=True, through='EmployeeServiceTypeSpecialty')


    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
