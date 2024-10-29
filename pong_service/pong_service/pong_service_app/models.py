from django.db import models
from django.utils import timezone

# def user_directory_path(instance, filename):
#     return 'avatars/{0}'.format(filename)

class PongUser(models.Model):
    user_id = models.IntegerField(primary_key=True, unique=True)
    game_history = models.JSONField(default=list)
    last_game = models.IntegerField(default="-1")

    def __str__(self):
        return str(self.user_id)
    
class PongGame(models.Model):
    type_choices = [("local1v1", "Local 1v1"), ("1v1", "1v1"), ("arcade", "Arcade"), ("tournament", "Tournament")]
    status_choices = [("init", "Init"), ("started", "Started"), ("finished", "Finished"), ("forfaited", "Forfaited")]

    game_id = models.AutoField(primary_key=True, unique=True)
    users = models.JSONField(default=list)
    winner_id = models.IntegerField(default=-1)
    score = models.JSONField(default=list)
    type = models.CharField(max_length=255, choices=type_choices, default="1v1")
    status = models.CharField(max_length=255, choices=status_choices, default="init")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.game_id)
    
class PongUserStats(models.Model):
    user_id = models.IntegerField(primary_key=True, unique=True)
    played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user_id)