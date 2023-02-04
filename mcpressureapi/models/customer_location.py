from django.db import models

class CustomerLocation(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    location = models.ForeignKey("Location", on_delete=models.CASCADE)