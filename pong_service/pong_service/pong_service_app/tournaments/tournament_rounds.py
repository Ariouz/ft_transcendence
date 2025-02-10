import random
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from pong_service_app.models import *
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
from pong_service_app.response_messages import success_response, error_response
import math
from asgiref.sync import async_to_sync, sync_to_async
from ..api.game import create_game
from ..api.objects import pong_game_state
from ..api.themes import get_theme, get_tournament_theme
from . import tournament_ws_utils


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

    if participant_count <= 2:
        return error_response(request, "No enough players", "Participant count must be > 2")

    tournament.total_rounds = math.ceil(math.log2(participant_count)) if participant_count > 0 else 0
    tournament.state = 'ongoing'
    tournament.save()

    rounds = generate_tournament_matches(tournament)

    tournament_ws_utils.send_tournament_started(tournament_id=tournament.tournament_id)

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


# /api/tournament/start-round/
@require_http_methods(["POST"])
def start_next_tournament_round(request):
    try:
        data = json.loads(request.body)
        tournament_id = data.get("tournament_id")
    except json.JSONDecodeError:
        return error_response(request, "invalid_json", "invalid_json")

    if not tournament_id:
        return error_response(request, "Missing parameter", "tournament_id missing")

    try:
        tournament = Tournament.objects.get(tournament_id=tournament_id)
    except Tournament.DoesNotExist:
        return error_response(request, "Tournament not found", "Tournament not found")

    if tournament.state != 'ongoing':
        return error_response(request, "Invalid tournament state", "Tournament is not ongoing")

    current_round = tournament.current_round

    matches = TournamentMatch.objects.filter(tournament=tournament, round=current_round)

    for match in matches:
        if match.pong_game is not None:
            return error_response(request, "Round already started", f"You must wait for all matches to be finished")

    game_ids = []
    for match in matches:
        players = [match.player1.user_id]
        if match.player2:
            players.append(match.player2.user_id)

        if match.player1 == match.player2:
            game = PongGame.objects.create(
                users=players, 
                type="classic", 
                map_theme=get_tournament_theme(), 
                winner_id=match.player1.user_id,
                status="finished",
                tournament_id=tournament_id
            )
            game.save()
            game_id = game.game_id
            logging.getLogger("django").info(f"Created finished game (same players): {players}")
        else:
            game_id = create_game(players, "classic", tournament_id=tournament_id, theme="tournament")
            game = PongGame.objects.get(game_id=game_id)
            logging.getLogger("django").info(f"Creating game with {players}")

        match.pong_game = game
        match.save()
        game_ids.append(game_id)

    return success_response(request, "Round started", extra_data={"game_ids": game_ids})


@sync_to_async
def update_tournament_match(game_state: pong_game_state.PongGameState):
    try:
        match = TournamentMatch.objects.get(pong_game=game_state.game_id)

        winner_id = game_state.get_player_id(game_state.get_winner())
        winner = PongUser.objects.get(user_id=winner_id)

        match.score1 = game_state.players['player1']['score']
        match.score2 = game_state.players['player2']['score']

        if match.score1 == 5 or match.score2 == 5:
            match.winner = winner
            pongloser = match.player1 if match.player1 != winner else match.player2
            if pongloser:
                loser = TournamentParticipant.objects.get(pong_user=pongloser, tournament=match.tournament)
                loser.eliminated = True
                loser.save()

        match.save()
        tournament_ws_utils.send_round_update(match)

        logging.getLogger("django").info(f"TournamentMatch updated for game {game_state.game_id}")
        check_round_completion(match.tournament)

    except TournamentMatch.DoesNotExist:
        logging.getLogger("django").info(f"No TournamentMatch found for game {game_state.game_id}")
    except PongUser.DoesNotExist:
        logging.getLogger("django").error(f"Winner not found for game {game_state.game_id}")
    except Exception as e:
        logging.getLogger("django").error(f"Error updating TournamentMatch: {e}")


def check_round_completion(tournament:Tournament):
    current_round = tournament.current_round
    matches_in_round = TournamentMatch.objects.filter(tournament=tournament, round=current_round)

    if all(match.winner is not None for match in matches_in_round):
        if current_round < tournament.total_rounds:
            tournament.current_round += 1
            tournament.save()
            generate_tournament_matches(tournament)
            logging.info(f"Round {current_round} completed. Starting round {tournament.current_round} generation.")

            tournament_ws_utils.send_rounds_generated(tournament.tournament_id)
        else:
            tournament.winner = TournamentParticipant.objects.filter(tournament=tournament, eliminated=False).get().pong_user
            tournament.state = "finished"
            tournament.save()
            logging.info(f"Tournament {tournament.tournament_id} finished.")
            tournament_ws_utils.send_tournament_ended(tournament.tournament_id, tournament.winner.user_id)
    else:
        logging.info(f"Round {current_round} is not yet completed.")


