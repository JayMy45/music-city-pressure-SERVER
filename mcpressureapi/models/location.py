from django.db import models

class Location(models.Model):
    street =  models.CharField(max_length=155)
    city = models.ForeignKey('City', on_delete=models.CASCADE)