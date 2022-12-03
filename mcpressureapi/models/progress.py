from django.db import models

class Progress(models.Model):
    label =  models.CharField(max_length=155)