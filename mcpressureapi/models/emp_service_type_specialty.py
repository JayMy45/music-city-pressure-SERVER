from django.db import models

class EmployeeServiceTypeSpecialty(models.Model):
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE, related_name='tools')
    specialty = models.ForeignKey("Specialty", on_delete=models.CASCADE)