from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneField(blank=True, help_text='Contact phone number')
    address = models.CharField(max_length=200)    
    location = models.ManyToManyField('Location', blank=True, through='CustomerLocation')
    image = models.CharField(max_length=500)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
