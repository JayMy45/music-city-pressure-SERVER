from django.db import models

class ServiceCall(models.Model):
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    service_type = models.ForeignKey("ServiceType", on_delete=models.CASCADE)
    progress = models.ForeignKey("Progress", on_delete=models.CASCADE)
    request_date = models.DateField()
    date_completed = models.DateField()
    consultation = models.BooleanField()
    completed = models.BooleanField() 