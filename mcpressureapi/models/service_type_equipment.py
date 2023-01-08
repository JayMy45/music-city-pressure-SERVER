from django.db import models

class ServiceTypeEquipment(models.Model):
    service_type = models.ForeignKey("ServiceType", on_delete=models.CASCADE)
    equipment = models.ForeignKey("Equipment", on_delete=models.CASCADE, related_name='tools')