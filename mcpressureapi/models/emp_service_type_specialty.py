from django.db import models

class EmployeeServiceTypeSpecialty(models.Model):
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE, related_name='technician')
    specialty = models.ForeignKey("Specialty", on_delete=models.CASCADE)