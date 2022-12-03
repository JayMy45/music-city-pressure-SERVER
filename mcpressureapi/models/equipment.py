from django.db import models

class Equipment(models.Model):
    label =  models.CharField(max_length=155)