from django.db import models
from django.db.models import Q

def user_directory_path(instance, filename):
    return 'avatars/{0}'.format(filename)

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
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True, default="avatars/default_avatar.svg")
    display_name = models.CharField(max_length=32)
    lang = models.CharField(max_length=2, default="en")
    github = models.CharField(max_length=255, default="null")
    status_message = models.CharField(max_length=128, default="Hello World")

    def __str__(self):
        return str(self.user_id)


class UserConfidentialitySettings(models.Model):
    visibility_choices = [("public", "Public"), ("private", "Private")]

    user_id = models.IntegerField(unique=True)
    profile_visibility = models.CharField(max_length=32, choices=visibility_choices, default="public")
    show_fullname = models.BooleanField(default=True)
    show_email = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user_id)


class Friend(models.Model):
    user = models.ForeignKey(
        User, related_name="user_friends", on_delete=models.CASCADE
    )
    friend = models.ForeignKey(
        User, related_name="friends_of", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}"
