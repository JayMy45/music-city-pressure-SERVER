from django.db import models

class CustomerConfirmAppointment(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, null=True, blank=True, related_name='confirmed')
    appointment = models.ForeignKey("Appointments", on_delete=models.CASCADE, null=True, blank=True, related_name='confirmed')