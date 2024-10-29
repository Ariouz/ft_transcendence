from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from pong_service_app.models import *
import ft_requests
import json
import logging
from .. import pong_user


@csrf_exempt
@require_http_methods(["GET"])
def user_history(request, user_id):
    offset = int(request.GET.get("offset"))
    limit = int(request.GET.get("limit"))

    if not offset:
        offset = 0
    if not limit:
        limit = 50

    if not PongUser.objects.filter(user_id=user_id).exists():
        return JsonResponse({"error":"User not found", "details": "No user found matching id"}, status=400)
    
    user = PongUser.objects.filter(user_id=user_id).get()
    history = list(reversed(user.game_history))

    if offset < 0:
        offset = 0
    if limit < 0:
        limit = 0

    if offset >= len(history):
        offset = len(history) - 1
    if offset + limit >= len(history):
        limit = len(history) - offset

    games = {}
    history = history[offset:offset+limit]

    for game_id in history:
        games[game_id] = {"data": game_id}
        game = PongGame.objects.filter(game_id=game_id).get()
        if not game:
            continue
        if game.status == "init":
            continue
        games[game_id] = {
            "game_id": game.game_id,
            "users": [int(i) for i in game.users],
            "winner_id": game.winner_id,
            "score": game.score,
            "type": game.type,
            "status": game.status,
            "date": game.date
        }

    return JsonResponse({"success":"History found", "user_id": user_id, "history": games})

    