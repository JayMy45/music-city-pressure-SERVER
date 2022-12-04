from django.db import models

class ServiceTypeEquipment(models.Model):
    equipment_id = models.ForeignKey("Equipment", on_delete=models.CASCADE, related_name='tools')
    service_type_id = models.ForeignKey("ServiceType", on_delete=models.CASCADE)