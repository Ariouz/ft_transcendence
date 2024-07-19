from django import forms
from django.db import models
from django.conf import settings


class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.username

class UserSettings(models.Model):
    user_id = models.IntegerField(unique=True)
    default_avatar = models.URLField()
    custom_avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user_id