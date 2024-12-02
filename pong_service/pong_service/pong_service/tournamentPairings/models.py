from django.db import models
from pong_service.pong_service_app.models import PongUser
from uuid import uuid4


# Create your models here.
class TournamentPairingData(models.Model):
    id = models.BigAutoField(primary_key=True)
    tournament_id = models.CharField(max_length=60, unique=False)
    player1 = models.ForeignKey(PongUser, on_delete=models.CASCADE, null=True, related_name='player1_id')
    player2 = models.ForeignKey(PongUser, on_delete=models.CASCADE, null=True, related_name='player2_id')
    winner = models.ForeignKey(PongUser, on_delete=models.CASCADE, null=True, related_name='winner_id')
    round_id = models.CharField(max_length=60, unique=False, blank=True, null=True)
    linkToJoin = models.UUIDField(default=uuid4, editable=False)

