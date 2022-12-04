from django.db import models

class ServiceType(models.Model):
    label = models.CharField(max_length=155)
    description = models.CharField(max_length=200)
    location = models.ForeignKey("Location", on_delete=models.CASCADE)
    price = models.FloatField()
    equipment_id = models.ForeignKey('Equipment', blank=True, on_delete=models.CASCADE)
    name =  models.CharField(max_length=75)