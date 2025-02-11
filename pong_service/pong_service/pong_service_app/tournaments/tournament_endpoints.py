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
        return error_response(request, "Missing parameter", "user_id_missing")

    if not PongUser.objects.filter(user_id=host_id).exists():
        create_user_if_not_exists(host_id)
        
    host = PongUser.objects.filter(user_id=host_id).get()

    # If already hosts another tournament
    if Tournament.objects.filter(host=host).exclude(state="finished").exists():
        return error_response(request, "error ", "tournament_already_hosts_another")

    # If already plays another active tournament
    if TournamentParticipant.objects.filter(pong_user=host, tournament__state__in=["pending", "ongoing"]).exists():
        return error_response(request, "tournament_error", "You already participate to another tournament")
    
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
        return error_response(request, "Missing parameter", "user_id_missing")
    
    if not tournament_id:
        return error_response(request, "Missing parameter", "tournament_id_missing")


    host = PongUser.objects.filter(user_id=user_id).first()
    if not host:
        return error_response(request, "Invalid host", "host_not_found")
    
    tournament = Tournament.objects.filter(tournament_id=tournament_id).first()
    if not tournament:
        return error_response(request, "tournament_error", "tournament_not_found")
    
    if tournament.host != host:
        return error_response(request, "tournament_error", "not_tournament_host")
    
    if tournament.state != "pending":
        return error_response(request, "tournament_error", "tournament_already_started")
    
    tournament_ws_utils.send_tournament_delete(tournament.tournament_id)
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
        return error_response(request, "tournament_error", "user_id_missing")
    
    if not tournament_id:
        return error_response(request, "tournament_error", "tournament_id_missing")
    
    if not PongUser.objects.filter(user_id=user_id).exists():
        create_user_if_not_exists(user_id)
        
    user = PongUser.objects.filter(user_id=user_id).get()
    
    tournament = Tournament.objects.filter(tournament_id=tournament_id).first()
    if not tournament:
        return error_response(request, "tournament_error", "tournament_not_found")

    if tournament.state != "pending":
        return error_response(request, "tournament_error", "tournament_already_started")

    if TournamentParticipant.objects.filter(tournament=tournament, pong_user=user).exists():
        return error_response(request, "tournament_error", "tournament_already_participates")

    if TournamentParticipant.objects.filter(pong_user=user, tournament__state__in=["ongoing", "pending"]).exists():
        return error_response(request, "tournament_error", "tournament_already_participates_another")
    

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
        return error_response(request, "Missing parameter", "user_id_missing")
    
    if not tournament_id:
        return error_response(request, "Missing parameter", "tournament_id_missing")
    
    if not PongUser.objects.filter(user_id=user_id).exists():
        create_user_if_not_exists(user_id)
        
    user = PongUser.objects.filter(user_id=user_id).get()
    
    tournament = Tournament.objects.filter(tournament_id=tournament_id).first()
    if not tournament:
        return error_response(request, "Invalid tournament", "tournament_not_found")

    if not TournamentParticipant.objects.filter(tournament_id=tournament_id, pong_user=user).exists():
        return error_response(request, "tournament_error", "tournament_doesnt_participate")

    if tournament.host == user:
        return error_response(request, "tournament_error", "tournament_host_cannot_leave")

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
        return error_response(request, "Missing parameter", "user_id_missing")
    
    if not tournament_id:
        return error_response(request, "Missing parameter", "tournament_id_missing")
    
    if not PongUser.objects.filter(user_id=user_id).exists():
        create_user_if_not_exists(user_id)
        
    user = PongUser.objects.filter(user_id=user_id).get()
    
    if not TournamentParticipant.objects.filter(tournament_id=tournament_id, pong_user=user).exists():
        return success_response(request, "tournament_doesnt_participate", extra_data={'participates':False})
    
    return success_response(request, "tournament_participate", extra_data={'participates':True})


# /api/tournament/state/
@require_http_methods(["POST"])
def tournament_state(request):
    try:
        data = json.loads(request.body)
        tournament_id = data.get("tournament_id")
    except:
        return error_response(request, "invalid_json", "invalid_json")

    if not tournament_id:
        return error_response(request, "Missing parameter", "tournament_id_missing")
    
    tournament = Tournament.objects.filter(tournament_id=tournament_id).get()
    if not tournament:
        return error_response(request, "Invalid tournament", "tournament_not_found")
    
    return success_response(request, "State retrieved", extra_data={"state":tournament.state})


# /api/tournament/list/
@require_http_methods(["POST"])
def tournament_list(request):
    tournaments = Tournament.objects.filter(state="pending").all()

    data = {}
    for tournament in tournaments:
        participantCount = TournamentParticipant.objects.filter(tournament=tournament).count()
        data[tournament.tournament_id] = {"tournament_id": tournament.tournament_id, 'player_count': participantCount}

    
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
        return error_response(request, "Missing parameter", "tournament_id_missing")
    
    tournament = Tournament.objects.filter(tournament_id=tournament_id).get()
    if not tournament:
        return error_response(request, "Invalid tournament", "tournament_not_found")

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
        return error_response(request, "Missing parameter", "user_id_missing")
    
    if not tournament_id:
        return error_response(request, "Missing parameter", "tournament_id_missing")
    
    if not PongUser.objects.filter(user_id=user_id).exists():
        create_user_if_not_exists(user_id)
        
    user = PongUser.objects.filter(user_id=user_id).get()
    
    if not TournamentParticipant.objects.filter(tournament_id=tournament_id, pong_user=user).exists():
        return error_response(request, "tournament_error", "tournament_doesnt_participate")
    
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
        return error_response(request, "Missing parameter", "user_id_missing")
    
    if not tournament_id:
        return error_response(request, "Missing parameter", "tournament_id_missing")
    
    tournament = Tournament.objects.filter(tournament_id=tournament_id).get()
    if not tournament:
        return error_response(request, "Invalid tournament", "tournament_not_found")

    if not PongUser.objects.filter(user_id=user_id).exists():
        return error_response(request, "Invalid user", "user_not_found")
        
    user = PongUser.objects.filter(user_id=user_id).get()
    
    if not TournamentParticipant.objects.filter(tournament_id=tournament_id, pong_user=user).exists():
        return error_response(request, "tournament_doesnt_participate")
    
    participant = TournamentParticipant.objects.filter(tournament_id=tournament_id, pong_user=user).get()
    if tournament.host != participant.pong_user:
        return error_response(request, "Invalid host", "not_tournament_host")
    
    return success_response(request, "User is host", extra_data={'is_host':True})


# /api/tournament/get-hosted/
@require_http_methods(["POST"])
def get_hosted_tournament(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
    except:
        return error_response(request, "invalid_json", "invalid_json")

    if not user_id:
        return error_response(request, "Missing parameter", "user_id_missing")

    try:
        user = PongUser.objects.get(user_id=user_id)
    except PongUser.DoesNotExist:
        return error_response(request, "user_not_found", "user_not_found")

    tournament = Tournament.objects.filter(host=user, state="pending").first()
    participant_count = 0
    tournament_id = -1

    if tournament:
        tournament_id = tournament.tournament_id
        participant_count = TournamentParticipant.objects.filter(tournament=tournament).count()
        
    return success_response(request, "Data retrieved", extra_data={
            "tournament_id": tournament_id,
            "participant_count": participant_count
        })
