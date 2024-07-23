from django import forms
from django.db import models
from django.conf import settings


class User(models.Model):
    user_id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=128, unique=True)
    fullname = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.username

class UserSettings(models.Model):
    user_id = models.IntegerField(unique=True)
    avatar = models.CharField(max_length=255)
    display_name = models.CharField(max_length=32)

    def __str__(self):
        return str(self.user_id) 