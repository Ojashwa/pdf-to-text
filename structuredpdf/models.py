from enum import auto
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Userregistration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50)

    # def __str__(self):
    #     return self.name

class Userpdfdata(models.Model):
    seller = models.CharField(max_length=500)
    buyer = models.CharField(max_length=500)
    invoice_number = models.CharField(max_length=100)
    invoice_date = models.CharField(max_length=100)
    items = models.CharField(max_length=500)
    digitalized = models.CharField(max_length=20)

    