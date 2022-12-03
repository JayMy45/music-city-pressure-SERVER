from django.db import models

class ServiceType(models.Model):
    label = models.CharField(max_length=155)
    description = models.CharField(max_length=200)
    location = models.ForeignKey("Location", on_delete=models.CASCADE)
    price = models.FloatField()
    tools = models.ManyToManyField('Equipment', blank=True, through='ServiceTypeEquipment')
    name =  models.CharField(max_length=75)