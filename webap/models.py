from django.db import models

# Create your models here.
class UserProfile(models.Model):
    identifier = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    meter_id = models.CharField(max_length=100)

class InformationHousehold(models.Model):
    LCLid = models.CharField(max_length=20)
    stdorToU = models.CharField(max_length=20)
    Acorn = models.CharField(max_length=20)
    Acorn_grouped = models.CharField(max_length=20)
    file = models.CharField(max_length=20)
