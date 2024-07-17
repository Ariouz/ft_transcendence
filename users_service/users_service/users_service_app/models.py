from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.username
