from django.db import models
from numpy import mod

# Create your models here.
class stocks_model(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name