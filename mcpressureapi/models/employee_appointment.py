from django.db import models

class EmployeeAppointment(models.Model):
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE, null=True, blank=True)
    appointment = models.ForeignKey("Appointments", on_delete=models.CASCADE, null=True, blank=True)