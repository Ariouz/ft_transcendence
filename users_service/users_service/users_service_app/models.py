from django.db import models


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
    lang = models.CharField(max_length=2, default="en")
    github = models.CharField(max_length=255, default="null")
    status_message = models.CharField(max_length=128, default="Hello World")

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
        constraints = [
            models.UniqueConstraint(fields=["user", "friend"], name="unique_friendship")
        ]

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}"
