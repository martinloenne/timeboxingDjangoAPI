# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
import datetime
import pytz

timezones = []

for tz in pytz.all_timezones:
    timezones.append((str(tz),tz))




class CustomUser(AbstractUser):
    pass

    bio = models.TextField(max_length=500, blank=True)
    timezone = models.CharField(max_length=255, choices=timezones, blank=True, null=True)
    startPage = models.TextField(max_length=9000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=50, default="public", blank=True, null=True)
    volume = models.DecimalField(default=0.7, blank=True, null=True,max_digits=5, decimal_places=2)
    def __str__(self):
        return self.email


class Category(models.Model):
    author = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE,
      blank=True,
      null=True,
      verbose_name = 'get_user_model',
    )
    name = models.CharField(max_length=50)
    baseCategory = models.BooleanField(blank=True, null=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    author = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE, 
    )
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Session(models.Model):
    author = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
    )
    sessionTime = models.IntegerField(null=True)    
    categoryTime = models.CharField(max_length=50)
    productTime = models.CharField(max_length=50)
    sessionDateTime = models.CharField(max_length=50)

    def __str__(self):
        return " Session :" + self.author.email


class Member(models.Model):
    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=40)
    age = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
 
    def __str__(self):
        return self.firstname + " " + self.lastname