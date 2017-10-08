# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Pollutants(models.Model):
    #serial_num=models.IntegerField()
    device_id=models.CharField(max_length=100)
    aqi=models.FloatField(max_length=20)
    so2=models.FloatField(max_length=20)
    no2=models.FloatField(max_length=20)
    o3=models.FloatField(max_length=20)
    hum=models.FloatField(max_length=20)
    temp=models.FloatField(max_length=20)
    co=models.FloatField(max_length=20)
    pm25=models.FloatField(max_length=20)
