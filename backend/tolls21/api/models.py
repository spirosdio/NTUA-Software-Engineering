from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User


# Create your models here.
class provider(models.Model) :
    user_id         = models.ForeignKey(User ,on_delete=models.CASCADE)
    provider_id     = models.CharField(max_length=50, primary_key=True)
    fullname        = models.CharField(max_length=50)

class vehicle(models.Model):
    vehicle_id      = models.CharField(max_length=50, primary_key=True)
    tag_id          = models.CharField(max_length=50, null=True)
    provider        = models.ForeignKey(provider, on_delete=models.CASCADE)
    license_year    = models.IntegerField()

class driver(models.Model):
    first_name      = models.CharField(max_length=45)
    last_name       = models.CharField(max_length=45)
    phoneNo         = models.CharField(max_length=15)
    birth_date      = models.DateField (blank=False)
    ssn             = models.IntegerField()
    vehicle         = models.ForeignKey(vehicle, on_delete=models.CASCADE, null=True)

class station(models.Model):
    station_id      =  models.CharField(max_length=50, primary_key=True)
    station_name    = models.CharField(max_length=50)
    provider        = models.ForeignKey(provider, on_delete=models.CASCADE)

class pass_event(models.Model):
    pass_id         = models.CharField(max_length=50, primary_key=True)
    timestamp       = models.DateTimeField(blank=False)
    vehicleRef      = models.ForeignKey(vehicle, on_delete=models.CASCADE)
    stationRef      = models.ForeignKey(station, on_delete=models.CASCADE)
    charge          = models.FloatField()