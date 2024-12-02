from django.db import models
from pong_service.pong_service_app.models import PongUser

# Create your models here.
class TournamentParticipants(models.Model):
    id = models.BigAutoField(primary_key=True)
    tournament_id = models.CharField(max_length=60, unique=False)
    user = models.ForeignKey(PongUser, on_delete=models.CASCADE, null=True)
    isEliminated = models.BooleanField(default=False)
