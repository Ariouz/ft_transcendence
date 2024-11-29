from rest_framework import serializers
from .models import TournamentPairingData

class TournamentPairingSerializer(serializers.ModelSerializer):
	player1_name = serializers.CharField(source='player1.email')
	player2_name = serializers.CharField(source='player2.email', default='')
	class Meta:
		model = TournamentPairingData
		fields = ['id', 'tournament_id', 'player1', 'player2', 'winner', 'round_id', 'linkToJoin', 'player1_name', 'player2_name']