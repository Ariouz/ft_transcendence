from django.views.decorators.http import require_http_methods
from pong_service_app.models import *
import json
from ..api.pong_user import create_user_if_not_exists

from pong_service_app.response_messages import success_response, error_response
from . import tournament_ws_utils

# /api/tournament/create/
@require_http_methods(["POST"])
def create_tournament(request):
    try:
        data = json.loads(request.body)
        host_id = data.get("host_id")
    except:
        return error_response(request, "invalid_json", "invalid_json")

    if not host_id:
        return error_response(request, "Missing parameter", "host_id missing")

    if not PongUser.objects.filter(user_id=host_id).exists():
        create_user_if_not_exists(host_id)
        
    host = PongUser.objects.filter(user_id=host_id).get()

    # If already hosts another tournament
    if Tournament.objects.filter(host=host).exclude(state="finished").exists():
        return error_response(request, "Already hosts a tournament", "An other tournament is hosted by this user")

    # If already plays another active tournament
    if TournamentParticipant.objects.filter(pong_user=host, tournament__state__in=["pending", "ongoing"]).exists():
        return error_response(request, "Already in ongoing tournament", "User already plays in another active tournament")
    
    tournament = Tournament.objects.create(host=host)
    TournamentParticipant.objects.create(tournament=tournament, pong_user=host)

    tournament_ws_utils.join_user(host.user_id, tournament.tournament_id)
    tournament_ws_utils.ws_connect_user(host.user_id, tournament.tournament_id)
    return success_response(request, "Tournament created", extra_data={"tournament_id":tournament.tournament_id})


# /api/tournament/delete/
@require_http_methods(["POST"])
def delete_tournament(request):
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


    host = PongUser.objects.filter(user_id=user_id).first()
    if not host:
        return error_response(request, "Invalid host", "Host user not found")
    
    tournament = Tournament.objects.filter(tournament_id=tournament_id).first()
    if not tournament:
        return error_response(request, "Invalid tournament", "Tournament not found")
    
    if tournament.host != host:
        return error_response(request, "Invalid host", "User is not the tournament's host")
    
    if tournament.state != "pending":
        return error_response(request, "Invalid state", "Tournament has already started")
    
    # TODO disconnect all users from tournament websocket
    tournament.delete()
    return success_response(request, "Tournament deleted")


# /api/tournament/join/
@require_http_methods(["POST"])
def join_tournament(request):
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
    
    if not PongUser.objects.filter(user_id=user_id).exists():
        create_user_if_not_exists(user_id)
        
    user = PongUser.objects.filter(user_id=user_id).get()
    
    tournament = Tournament.objects.filter(tournament_id=tournament_id).first()
    if not tournament:
        return error_response(request, "Invalid tournament", "Tournament not found")

    if tournament.state != "pending":
        return error_response(request, "Invalid state", "Tournament has already started")

    if TournamentParticipant.objects.filter(tournament_id=tournament_id, pong_user=user).exists():
        return error_response(request, "Already a participant", "You already participate to this tournament")
    

    TournamentParticipant.objects.create(tournament=tournament, pong_user=user)
    tournament_ws_utils.join_user(user.user_id, tournament.tournament_id)
    tournament_ws_utils.ws_connect_user(user.user_id, tournament.tournament_id)
    return success_response(request, "Joined tournament", extra_data={"tournament_id":tournament_id})


# /api/tournament/leave/
@require_http_methods(["POST"])
def leave_tournament(request):
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
    
    if not PongUser.objects.filter(user_id=user_id).exists():
        create_user_if_not_exists(user_id)
        
    user = PongUser.objects.filter(user_id=user_id).get()
    
    tournament = Tournament.objects.filter(tournament_id=tournament_id).first()
    if not tournament:
        return error_response(request, "Invalid tournament", "Tournament not found")

    if not TournamentParticipant.objects.filter(tournament_id=tournament_id, pong_user=user).exists():
        return error_response(request, "Not a participant", "You don't participate to this tournament")

    if tournament.host == user:
        return error_response(request, "Cannot delete", "Tournament's host cannot leave the tournament. You need to delete it")

    TournamentParticipant.objects.filter(tournament=tournament, pong_user=user).delete()
    tournament_ws_utils.ws_disconnect_user(user_id, tournament_id)

    return success_response(request, "Left tournament", extra_data={"tournament_id":tournament_id})


# /api/tournament/does-participates/
@require_http_methods(["POST"])
def does_participates(request):
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
    
    if not PongUser.objects.filter(user_id=user_id).exists():
        create_user_if_not_exists(user_id)
        
    user = PongUser.objects.filter(user_id=user_id).get()
    
    if not TournamentParticipant.objects.filter(tournament_id=tournament_id, pong_user=user).exists():
        return success_response(request, "User doesn't participates", extra_data={'participates':False})
    
    return success_response(request, "User participates", extra_data={'participates':True})


# /api/tournament/state/
@require_http_methods(["POST"])
def tournament_state(request):
    try:
        data = json.loads(request.body)
        tournament_id = data.get("tournament_id")
    except:
        return error_response(request, "invalid_json", "invalid_json")

    if not tournament_id:
        return error_response(request, "Missing parameter", "tournament_id missing")
    
    tournament = Tournament.objects.filter(tournament_id=tournament_id).get()
    if not tournament:
        return error_response(request, "Invalid tournament", "Tournament not found")
    
    return success_response(request, "State retrieved", extra_data={"state":tournament.state})


# /api/tournament/list/
@require_http_methods(["POST"])
def tournament_list(request):
    tournaments = Tournament.objects.filter(state="pending").all()

    data = {}
    for tournament in tournaments:
        data[tournament.tournament_id] = {"tournament_id": tournament.tournament_id}
    
    return success_response(request, "List retrieved", extra_data={"data":data})


# /api/tournament/participants/
@require_http_methods(["POST"])
def tournament_participants(request):
    try:
        data = json.loads(request.body)
        tournament_id = data.get("tournament_id")
    except:
        return error_response(request, "invalid_json", "invalid_json")

    if not tournament_id:
        return error_response(request, "Missing parameter", "tournament_id missing")
    
    tournament = Tournament.objects.filter(tournament_id=tournament_id).get()
    if not tournament:
        return error_response(request, "Invalid tournament", "Tournament not found")

    data = []
    for tournament_participant in TournamentParticipant.objects.filter(tournament=tournament).all():
        data.append(tournament_participant.pong_user.user_id)
    
    return success_response(request, "List retrieved", extra_data={"participants":data})


# /api/tournament/ws_connect/
@require_http_methods(["POST"])
def ws_connect(request):
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
    
    if not PongUser.objects.filter(user_id=user_id).exists():
        create_user_if_not_exists(user_id)
        
    user = PongUser.objects.filter(user_id=user_id).get()
    
    if not TournamentParticipant.objects.filter(tournament_id=tournament_id, pong_user=user).exists():
        return error_response(request, "Cannot connect to ws", "User doesn't participates")
    
    tournament_ws_utils.ws_connect_user(user_id, tournament_id)
    return success_response(request, "Connected successfully", extra_data={'tournament_id':tournament_id})


# /api/tournament/is-host/
@require_http_methods(["POST"])
def is_host(request):
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
    if not tournament:
        return error_response(request, "Invalid tournament", "Tournament not found")

    if not PongUser.objects.filter(user_id=user_id).exists():
        return error_response(request, "Invalid user", "User not found")
        
    user = PongUser.objects.filter(user_id=user_id).get()
    
    if not TournamentParticipant.objects.filter(tournament_id=tournament_id, pong_user=user).exists():
        return error_response(request, "User doesn't participates")
    
    participant = TournamentParticipant.objects.filter(tournament_id=tournament_id, pong_user=user).get()
    if tournament.host != participant.pong_user:
        return error_response(request, "Invalid host", "User isn't host")
    
    return success_response(request, "User is host", extra_data={'is_host':True})