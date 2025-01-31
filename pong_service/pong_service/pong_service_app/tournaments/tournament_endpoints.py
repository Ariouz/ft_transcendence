from django.views.decorators.http import require_http_methods
from pong_service_app.models import *
from concurrent.futures import ThreadPoolExecutor
import json
import logging
import asyncio

from pong_service_app.response_messages import success_response, error_response

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

    host = PongUser.objects.filter(user_id=host_id).get()
    if not host:
        return error_response(request, "Invalid host", "Host user not found")

    # If already hosts another tournament
    if Tournament.objects.filter(host=host).exclude(state="finished").exists():
        return error_response(request, "Already hosts a tournament", "An other tournament is hosted by this user")

    # If already plays another active tournament
    if TournamentParticipant.objects.filter(pong_user=host, tournament__state__in=["pending", "ongoing"]).exists():
        return error_response(request, "Already in ongoing tournament", "User already plays in another active tournament")
    
    tournament = Tournament.objects.create(host=host)
    TournamentParticipant.objects.create(tournament=tournament, pong_user=host)

    return success_response(request, "Tournament created successfully", extra_data={"tournament_id":tournament.tournament_id})


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
    
    tournament.delete()
    return success_response(request, "Tournament deleted")


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
    
    user = PongUser.objects.filter(user_id=user_id).get()
    if not user:
        return error_response(request, "Invalid user", "User not found")
    
    if not TournamentParticipant.objects.filter(tournament_id=tournament_id, pong_user=user).exists():
        return success_response(request, "User doesn't participates", extra_data={'participates':False})
    
    return success_response(request, "User participates", extra_data={'participates':True})


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