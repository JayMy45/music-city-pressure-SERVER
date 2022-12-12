from django.db import models

class ServiceType(models.Model):
    name =  models.CharField(max_length=75)
    label = models.CharField(max_length=155, null=True, blank=True)
    description = models.CharField(max_length=200)
    details = models.CharField(max_length=300)
    price = models.FloatField(null=True, blank=True)
    equipment_id = models.ForeignKey('Equipment', null=True, blank=True, on_delete=models.CASCADE)