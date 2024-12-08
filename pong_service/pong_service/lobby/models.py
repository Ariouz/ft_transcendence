from django.db import models
from django.contrib.postgres.fields import ArrayField
from pong_service_app.models import PongUser
from uuid import uuid4

# Create your models here.
class LobbyData(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=60, unique=False)
    lobbyWinner = models.ForeignKey(PongUser, on_delete=models.CASCADE, null=True, related_name='winner_lobby')
    # isPrivate = models.BooleanField(default=False,blank=True, null=True)
    # difficultyLevel = models.PositiveIntegerField(default=0,blank=True, null=True)
    isActiveLobby = models.BooleanField(default=True,blank=True, null=True)
    # pointsPerGame = models.PositiveIntegerField(default=0,blank=True, null=True)
    # timer = models.PositiveIntegerField(default=0,blank=True, null=True)
    # powerUps = models.BooleanField(default=False,blank=True, null=True)
    round = models.PositiveIntegerField(default=0,blank=True, null=True)
    linkToJoin = models.UUIDField(default=uuid4, editable=False)
    player1 = models.ForeignKey(PongUser, on_delete=models.CASCADE, null=True, related_name='lobby_player1')
    player2 = models.ForeignKey(PongUser, on_delete=models.CASCADE, null=True, related_name='lobby_player2')


