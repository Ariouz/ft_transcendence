from django.db import models
from django.utils import timezone
from .api.themes import get_default_theme

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
    map_theme = models.JSONField(default=get_default_theme)

    def __str__(self):
        return str(self.game_id)
    
class PongUserStats(models.Model):
    user_id = models.IntegerField(primary_key=True, unique=True)
    played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user_id)
    
class Tournament(models.Model):
    tournament_id = models.AutoField(primary_key=True, unique=True)
    state = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('finished', 'Finished')
    ], default='pending')
    winner = models.ForeignKey(PongUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_tournaments')
    host = models.ForeignKey(PongUser, on_delete=models.CASCADE, related_name='hosted_tournaments')
    created_at = models.DateTimeField(default=timezone.now)

class TournamentParticipant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="participants")
    pong_user = models.ForeignKey(PongUser, on_delete=models.CASCADE)
    eliminated = models.BooleanField(default=False)

    class Meta:
        unique_together = ('tournament', 'pong_user')

class TournamentMatch(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player1 = models.ForeignKey(PongUser, on_delete=models.CASCADE, related_name='matches_as_player1')
    player2 = models.ForeignKey(PongUser, on_delete=models.CASCADE, related_name='matches_as_player2')
    winner = models.ForeignKey(PongUser, on_delete=models.SET_NULL, null=True, blank=True)
    round = models.IntegerField()
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)