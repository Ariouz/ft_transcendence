from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer, OpenApiResponse
from rest_framework import serializers

from .models import TournamentData
from tournamentParticipants.models import TournamentParticipants
from .serializers import TournamentSerializer
from tournamentParticipants.serializers import TournamentParticipantsSerializer
from rest_framework import status

import random

# Create your views here.
class TournamentView(APIView):
	def get(self, request):
		tournament = TournamentData.objects.filter(Q(tournamentWinner__isnull=True) | Q(tournamentWinner = None))
		serializer = TournamentSerializer(tournament, many=True)
		return Response(serializer.data)

	@extend_schema(
    request=inline_serializer(
        name="InlineFormSerializer",
        fields={
            "name": serializers.CharField(),
            "numberOfPlayers": serializers.CharField(),
			"isPrivate": serializers.BooleanField(),
			"difficultyLevel": serializers.CharField(),
			"isActiveTournament": serializers.BooleanField(),
			"pointsPerGame": serializers.CharField(),
			"timer": serializers.CharField(),
			"powerUps": serializers.BooleanField(),
        },
    ),
    description="create tournament",
    responses={
       200: inline_serializer(
           name='CreateTournamentresponse',
           fields={
               'message': serializers.CharField(),
           }
       ), 
       400: OpenApiResponse(description='user not found'),
    }
	)	
	
	def post(self, request):
		data = request.data
		if 'powerUps' in data:
			powerUpsData = data["powerUps"]
		else:
			powerUpsData=False
		
		print(data)
		new_tournament = TournamentData.objects.create(
			name=data['name'], 
			numberOfPlayers=data['numberOfPlayers'], 
			isPrivate=data['isPrivate'],
			difficultyLevel=data['difficultyLevel'],
			isActiveTournament=data['isActiveTournament'],
			pointsPerGame=data['pointsPerGame'],
			timer=data['timer'], 
			powerUps=powerUpsData
		)

		return Response({'message':'You have created tournament successfully'}, status=status.HTTP_201_CREATED)	


class TournamentDetailView(APIView):
	def get(self, request, id):
		tournament = TournamentData.objects.filter(id=id)
		tournamentParticpant = TournamentParticipants.objects.filter(tournament_id=id)
		serializer = TournamentSerializer(tournament, many=True)
		serializerT = TournamentParticipantsSerializer(tournamentParticpant, many=True)
		if(len(serializer.data) != 0):
			return Response({'data': {'detail': serializer.data, 'particpants': serializerT.data }}, status=status.HTTP_201_CREATED)	
		else:
			return Response({'message': 'Record not found with this Id.'}, status=status.HTTP_404_NOT_FOUND)


class TournamentGetView(APIView):
	def get(self, request):
		query = Q(tournamentWinner__isnull=True)
		query.add(Q(tournamentWinner = None), Q.OR)
		tournament = TournamentData.objects.filter(query)
		serializer = TournamentSerializer(tournament, many=True)
		return Response({'data': {'tournaments': serializer.data}}, status=status.HTTP_201_CREATED)	
