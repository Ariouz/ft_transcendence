from rest_framework import serializers
from .models import TournamentData

class TournamentSerializer(serializers.ModelSerializer):
	class Meta:
		model = TournamentData
		fields = ['id', 'name', 'numberOfPlayers', 'tournamentWinner', 'isPrivate', 'difficultyLevel', 'isActiveTournament', 'pointsPerGame', 'timer', 'powerUps', 'round']