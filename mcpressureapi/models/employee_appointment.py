from django.db import models

class EmployeeAppointment(models.Model):
    employee_id = models.ForeignKey("Employee", on_delete=models.CASCADE, null=True, blank=True)
    appointment_id = models.ForeignKey("Appointments", on_delete=models.CASCADE, null=True, blank=True)