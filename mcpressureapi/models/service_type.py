from django.db import models

class ServiceType(models.Model):
    label = models.CharField()
    description = models.CharField()
    location = models.ForeignKey("Location", on_delete=models.CASCADE)
    price = models.FloatField()
    name =  models.CharField()