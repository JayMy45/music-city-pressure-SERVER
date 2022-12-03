from django.db import models

class EmployeeServiceTypeSpecialty(models.Model):
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE, related_name='tools')
    service_type = models.ForeignKey("ServiceType", on_delete=models.CASCADE)
    specialty = models.ForeignKey("Specialty", on_delete=models.CASCADE)