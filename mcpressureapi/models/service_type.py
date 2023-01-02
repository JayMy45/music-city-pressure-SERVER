from django.db import models

class ServiceType(models.Model):
    name =  models.CharField(max_length=75)
    label = models.CharField(max_length=155, null=True, blank=True)
    image = models.CharField(max_length=400)
    description = models.CharField(max_length=200)
    details = models.CharField(max_length=300)
    price = models.FloatField(null=True, blank=True)
    tools = models.ManyToManyField('Equipment', blank=True, related_name="equipment_id", through='ServiceTypeEquipment')
    # attendees = models.ManyToManyField('Gamer', blank=True, through='GamerEvent')
