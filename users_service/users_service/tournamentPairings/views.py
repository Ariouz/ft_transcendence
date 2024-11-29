from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from .models import TournamentPairingData
from tournament.models import TournamentData
from users.models import User
from .serializers import TournamentPairingSerializer
from tournament.serializers import TournamentSerializer
from tournamentParticipants.models import TournamentParticipants
from tournamentParticipants.serializers import TournamentParticipantsSerializer
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist



import random

# Create your views here.
class CreateMatchMakingView(APIView):
	def pop_random(self, lst):
		idx = random.sample(lst, 1)
		return idx

	def get(self, request, id, roundId):
		tournamentPairings = TournamentPairingData.objects.filter(tournament_id=id, round_id=roundId)
		serializerPairings = TournamentPairingSerializer(tournamentPairings, many=True)
		if(len(serializerPairings.data) > 0):
			return Response({'particpants': serializerPairings.data }, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'No record found with this tourmentID,  roundId' }, status=status.HTTP_201_CREATED)

	def post(self, request, id, roundId):
		data = request.data
		tournamentParticpant = TournamentParticipants.objects.filter(tournament_id=id, isEliminated = False)
		serializerT = TournamentParticipantsSerializer(tournamentParticpant, many=True)
		particpantsData = serializerT.data
		tournamentData = TournamentData.objects.filter(id=id)
		print("particpantsData", particpantsData)
		while len(particpantsData) != 0:
			rand1 = self.pop_random(particpantsData)
			particpantsData.remove(rand1[0])
			try:
				user = User.objects.get(id=rand1[0]['uuid'])
			except ObjectDoesNotExist:
				return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

			if(len(particpantsData) >= 1):
				rand2 = self.pop_random(particpantsData)
				particpantsData.remove(rand2[0])
				try:
					user2 = User.objects.get(id=rand2[0]['uuid'])
				except ObjectDoesNotExist:
					return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
			else:
				user2 = None
				
			particpantPairing = TournamentPairingData.objects.create(tournament_id = id, player1 =user, player2 = user2, round_id = roundId)
			tournamentData.update(round=roundId)
			
		return Response({'message': 'Pairing for particpants has been created.' }, status=status.HTTP_201_CREATED)	

class UpdateWinnerView(APIView):
	def put(self, request):
		data = request.data
		query = Q(player1_id=data["winner_id"])
		query.add(Q(player2_id=data["winner_id"]), Q.OR)
		query.add(Q(tournament_id=data["tournament_id"]), Q.AND)
		query.add(Q(round_id = data["round_id"]), Q.AND)

		tournamentPairings = TournamentPairingData.objects.filter(query)
		serializerPairings = TournamentPairingSerializer(tournamentPairings, many=True)

		if (len(serializerPairings.data) > 0 and int(serializerPairings.data[0]['player1']) == int(data["winner_id"])):
			tournamentParticpants = TournamentParticipants.objects.filter(tournament_id=data["tournament_id"], user_id=serializerPairings.data[0]['player2'])
			serializerTournament = TournamentParticipantsSerializer(tournamentParticpants, many=True)
			tournamentParticpants.update(isEliminated=True)
		elif(len(serializerPairings.data) > 0 and int(serializerPairings.data[0]['player2']) == int(data["winner_id"])):
			tournamentParticpants = TournamentParticipants.objects.filter(tournament_id=data["tournament_id"], user_id=serializerPairings.data[0]['player1'])
			serializerTournament = TournamentParticipantsSerializer(tournamentParticpants, many=True)
			tournamentParticpants.update(isEliminated=True)


		tournamentParticpantsData = TournamentParticipants.objects.filter(tournament_id=data["tournament_id"], isEliminated=False)
		serializerTournamentPartiData = TournamentParticipantsSerializer(tournamentParticpantsData, many=True)
		
		try:
			user = User.objects.get(id=data["winner_id"])
			tournamentPairings.update(winner=user)
			if(len(serializerTournamentPartiData.data) == 1):
				tournamentData = TournamentData.objects.filter(id=data["tournament_id"])
				tournamentData.update(tournamentWinner=user)
		except ObjectDoesNotExist:
			return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
		
		return Response({'message': 'Winner has been updated' }, status=status.HTTP_201_CREATED)	

class FilterView(APIView):
	def get(self, request, UDID):
		tournamentPairings = TournamentPairingData.objects.filter(linkToJoin=UDID)
		serializerPairings = TournamentPairingSerializer(tournamentPairings, many=True)
		if(len(serializerPairings.data) > 0):
			tournament = TournamentData.objects.filter(id=serializerPairings.data[0]['tournament_id'])
			serializerTournament = TournamentSerializer(tournament, many=True)
			return Response(serializerTournament.data[0], status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'No record found with this UDID' }, status=status.HTTP_201_CREATED)




	

