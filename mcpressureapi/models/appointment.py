from django.db import models

class Appointments(models.Model):
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, null=True, blank=True)
    service_type = models.ForeignKey("ServiceType", null=True, blank=True, on_delete=models.CASCADE)
    progress = models.ForeignKey("Progress", null=True, blank=True, on_delete=models.CASCADE)
    request_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    scheduled = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    consultation = models.BooleanField(default=False)
    completed = models.BooleanField(default=False) 
    request_details = models.CharField(max_length=200)
    
    # on the fence about locations...
    # location = models.ForeignKey("Location", on_delete=models.CASCADE)
