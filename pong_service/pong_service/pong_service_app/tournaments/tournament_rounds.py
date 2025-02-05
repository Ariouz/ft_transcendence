import random
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from pong_service_app.models import *
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
from pong_service_app.response_messages import success_response, error_response
import math


# /api/tournament/launch/
@require_http_methods(["POST"])
def launch_tournament(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        tournament_id = data.get("tournament_id")
    except:
        return error_response(request, "invalid_json", "invalid_json")

    if not user_id:
        return error_response(request, "Missing parameter", "user_id missing")

    if not tournament_id:
        return error_response(request, "Missing parameter", "tournament_id missing")
    
    tournament = Tournament.objects.filter(tournament_id=tournament_id).get()
    host = PongUser.objects.filter(user_id=user_id).first()
    if not host:
        return error_response(request, "Invalid host", "Host user not found")
    
    if tournament.host != host:
        return error_response(request, "Invalid host", "User is not the tournament's host")

    if tournament.state != 'pending':
        return error_response(request, "Tournament cannot be launched in its current state", "Tournament isn't pending")

    participant_count = TournamentParticipant.objects.filter(tournament=tournament).count()

    # if participant_count <= 2:
    #     return error_response(request, "No enough players", "Participant count must be > 2")

    tournament.total_rounds = math.ceil(math.log2(participant_count)) if participant_count > 0 else 0
    tournament.state = 'ongoing'
    tournament.save()

    rounds = generate_tournament_matches(tournament)

    return success_response(request, "Tournament launched successfully", extra_data={"tournament_rounds": rounds})


def generate_tournament_matches(tournament: Tournament):
    participants = TournamentParticipant.objects.filter(tournament=tournament, eliminated=False)
    players = [participant.pong_user for participant in participants]

    if len(players) % 2 != 0:
        qualified_player = random.choice(players)
        players.remove(qualified_player)
        TournamentMatch.objects.create(
            tournament=tournament,
            player1=qualified_player,
            player2=qualified_player,
            winner=qualified_player,
            round=tournament.current_round
        )

    random.shuffle(players)

    matches = []
    for i in range(0, len(players), 2):
        player1 = players[i]
        player2 = players[i + 1] if i + 1 < len(players) else None
        match = TournamentMatch.objects.create(
            tournament=tournament,
            player1=player1,
            player2=player2,
            round=tournament.current_round
        )
        matches.append(match)

    match_data = [{
        'player1': match.player1.user_id,
        'player2': match.player2.user_id if match.player2 else None,
        'round': match.round,
        'match_id': match.pk
    } for match in matches]

    previous_matches = TournamentMatch.objects.filter(tournament=tournament, round__lt=tournament.current_round)
    previous_results = [{
        'player1': match.player1.user_id,
        'player2': match.player2.user_id if match.player2 else None,
        'winner': match.winner.user_id if match.winner else None,
        'score1': match.score1,
        'score2': match.score2,
        'round': match.round,
        'match_id': match.pk
    } for match in previous_matches]

    response_data = {
        'current_round': tournament.current_round,
        'total_rounds': tournament.total_rounds,
        'matches': match_data,
        'previous_results': previous_results
    }

    return response_data

# /api/tournament/get-rounds/
@require_http_methods(["POST"])
def get_tournament_rounds(request):
    try:
        data = json.loads(request.body)
        tournament_id = data.get("tournament_id")
    except:
        return error_response(request, "invalid_json", "invalid_json")

    if not tournament_id:
        return error_response(request, "Missing parameter", "tournament_id missing")
    
    tournament = Tournament.objects.filter(tournament_id=tournament_id).get()

    rounds_data = []
    for round_num in range(1, tournament.current_round + 1):
        matches = TournamentMatch.objects.filter(tournament=tournament, round=round_num)
        round_completed = all(match.winner is not None for match in matches)
        
        match_data = []
        for match in matches:
            match_data.append({
                "match_id": match.pk,
                "player1": match.player1.user_id,
                "player2": match.player2.user_id if match.player2 else None,
                "winner": match.winner.user_id if match.winner else None,
                "score1": match.score1,
                "score2": match.score2,
                "ended": match.winner is not None
            })

        rounds_data.append({
            "round_number": round_num,
            "completed": round_completed,
            "matches": match_data,
            'current_round': tournament.current_round,
            'total_rounds': tournament.total_rounds,
        })

    return JsonResponse({"rounds": rounds_data})