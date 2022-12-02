from django.db import models

class Location(models.Model):
    label =  models.CharField(max_length=155)