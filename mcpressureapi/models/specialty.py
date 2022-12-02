from django.db import models

class Specialty(models.Model):
    label = models.CharField(max_length=75)