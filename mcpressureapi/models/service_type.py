from django.db import models

class ServiceType(models.Model):
    name =  models.CharField(max_length=75)
    label = models.CharField(max_length=155)
    description = models.CharField(max_length=200)
    details = models.CharField(max_length=300)
    price = models.FloatField()
    equipment_id = models.ForeignKey('Equipment', blank=True, on_delete=models.CASCADE)