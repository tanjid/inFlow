from email.policy import default
from enum import unique
from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=30,)
    mobile = models.CharField(max_length=20)
    tittle = models.CharField(max_length=50)
    address = models.CharField(max_length=300)
    logo = models.ImageField(upload_to='company/')
    fav_logo = models.ImageField(upload_to='company/')
    invoice_slug = models.CharField(max_length=300)
    invoice_count = models.IntegerField(default=1)
    def __str__(self):
        return self.name