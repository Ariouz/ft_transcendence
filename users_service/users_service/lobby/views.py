from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer, OpenApiResponse
from rest_framework import serializers

from .models import LobbyData
from .serializers import LobbySerializer
from users.models import User
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

import random

# Create your views here.
class LobbyView(APIView):
	def get(self, request):
		lobby = LobbyData.objects.filter(Q(lobbyWinner__isnull=True) | Q(lobbyWinner = None))
		serializer = LobbySerializer(lobby, many=True)
		return Response(serializer.data)

	@extend_schema(
    request=inline_serializer(
        name="InlineFormSerializer",
        fields={
					"name": serializers.CharField(),
					# "isPrivate": serializers.BooleanField(),
					# "difficultyLevel": serializers.CharField(),
					"isActiveLobby": serializers.BooleanField(),
					# "pointsPerGame": serializers.CharField(),
					# "timer": serializers.CharField(),
					# "powerUps": serializers.BooleanField(),
					"user_id": serializers.CharField(),
        },
    ),
    description="create Lobby",
    responses={
       200: inline_serializer(
           name='CreateLobbyresponse',
           fields={
               'message': serializers.CharField(),
           }
       ), 
       400: OpenApiResponse(description='user not found'),
    }
	)
	def post(self, request):
			data = request.data
			try:
				user = User.objects.get(id=data['uuid'])
				new_lobby = LobbyData.objects.create(
					name=data['name'],
					# isPrivate=data['isPrivate'],
					# difficultyLevel=data['difficultyLevel'],
					# pointsPerGame=data['pointsPerGame'],
					# timer=data['timer'],
					# powerUps=data['powerUps'],
					player1=user
				)
				serializer = LobbySerializer(new_lobby)
				return Response({'lobby': serializer.data}, status=status.HTTP_201_CREATED)	
			except ObjectDoesNotExist:
				return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

class LobbyGameView(APIView):
	def get(self, request):
		lobby = LobbyData.objects.filter(Q(isActiveLobby=True))
		serializer = LobbySerializer(lobby, many=True)
		return Response(serializer.data)

class LobbyUpdateView(APIView):
	def put(self,request, lobby_id, user_id):
		lobbyData = LobbyData.objects.filter(id=lobby_id)
		serializerLobby = LobbySerializer(lobbyData, many=True)

		if(serializerLobby.data[0]['isActiveLobby'] == True):
			try:
				user = User.objects.get(uuid=user_id)
				lobbyData.update(player2=user)
				lobbyData.update(isActiveLobby=False)
				return Response({'message':'You have updated player2 successfully'}, status=status.HTTP_201_CREATED)	
			except ObjectDoesNotExist:
				return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
		else:		
			return Response({'message': 'Lobby has already 2 players'}, status=status.HTTP_404_NOT_FOUND)






	

