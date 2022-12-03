from django.db import models

class ServiceCall(models.Model):
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, null=True, blank=True)
    service_type = models.ForeignKey("ServiceType", on_delete=models.CASCADE)
    progress = models.ForeignKey("Progress", on_delete=models.CASCADE)
    request_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    date_completed = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    consultation = models.BooleanField(default=False)
    completed = models.BooleanField(default=False) 