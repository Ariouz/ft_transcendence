from rest_framework import serializers
from .models import LobbyData

class LobbySerializer(serializers.ModelSerializer):
	class Meta:
		model = LobbyData
		fields = ['id', 'name', 'lobbyWinner', 'isActiveLobby', 'round', 'linkToJoin', 'player1', 'player2']