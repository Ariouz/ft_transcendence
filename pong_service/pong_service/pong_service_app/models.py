from django.db import models

# def user_directory_path(instance, filename):
#     return 'avatars/{0}'.format(filename)

class PongUser(models.Model):
    user_id = models.IntegerField(primary_key=True, unique=True)
    game_history = models.JSONField(default=list)

    def __str__(self):
        return self.user_id
    
class PongGame(models.Model):
    type_choices = [("1v1", "1v1"), ("tournament", "Tournament")]

    game_id = models.AutoField(primary_key=True, unique=True)
    users = models.JSONField(default=list)
    winner_id = models.IntegerField(blank=True)
    score = models.JSONField(default=list)
    type = models.CharField(max_length=255, choices=type_choices, default="1v1")

    def __str__(self):
        return self.game_id
    
class PongUserStats(models.Model):
    user_id = models.IntegerField(primary_key=True, unique=True)
    played = models.IntegerField()
    wins = models.IntegerField()
    loses = models.IntegerField()

    def __str__(self):
        return self.user_id