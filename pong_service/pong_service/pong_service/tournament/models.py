from django.db import models
from django.contrib.postgres.fields import ArrayField
from pong_service.pong_service_app.models import PongUser

# Create your models here.
class TournamentData(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=60, unique=False)
    numberOfPlayers = models.PositiveIntegerField(default=0,blank=True, null=True)
    isPrivate = models.BooleanField(default=False,blank=True, null=True)
    difficultyLevel = models.PositiveIntegerField(default=0,blank=True, null=True)
    isActiveTournament = models.BooleanField(default=False,blank=True, null=True)
    pointsPerGame = models.PositiveIntegerField(default=0,blank=True, null=True)
    timer = models.PositiveIntegerField(default=0,blank=True, null=True)
    powerUps = models.BooleanField(default=False,blank=True, null=True)
    round = models.PositiveIntegerField(default=0,blank=True, null=True)

