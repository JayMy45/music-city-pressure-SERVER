from django.db import models

class Reviews(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    service_call = models.ForeignKey("ServiceCall", on_delete=models.CASCADE)
    content = models.CharField(max_length=200)