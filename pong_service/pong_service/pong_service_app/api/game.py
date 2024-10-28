from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from pong_service_app.models import *
from concurrent.futures import ThreadPoolExecutor
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
import ft_requests
import redis
import json
import logging
from . import game_manager
import asyncio

executor = ThreadPoolExecutor()

@csrf_exempt
@require_http_methods(["GET"])
def get_game_data(request):
    game_id = request.GET.get("game_id")

    if game_id is None:
        return JsonResponse({"error":"No game id", "details": "A game_id is required"})

    if not PongGame.objects.filter(game_id=game_id).exists():
        return JsonResponse({"error":"Game not found", "details": "No game found matching id"})
    
    game = PongGame.objects.get(game_id=game_id)

    data = {
        "game_id": game_id,
        "players": game.users,
        "status": game.status,
        "type": game.type,
        "score": game.score,
        "winner_id": game.winner_id
    }
    return JsonResponse({"success": "Data retrieved", "data": data})

@csrf_exempt
@require_http_methods(["POST"])
def start_game(request):

    logging.getLogger("django").info(f"Received start request")
    try:
        data = json.loads(request.body)
        game_id = data.get("game_id")
    except:
        return JsonResponse({"error":"No game id", "details": "A game_id is required"}, status=400)

    if not PongGame.objects.filter(game_id=game_id).exists():
        logging.getLogger("django").info(f"Game not found {game_id}")
        return JsonResponse({"error":"Game not found", "details": "No game found matching id"}, status=400)
    
    logging.getLogger("django").info(f"Starting game {game_id}")
    run_start_game(game_id)
    
    return JsonResponse({"success": "Games started"})


@csrf_exempt
@require_http_methods(["POST"])
def create_local_game(request):

    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
    except:
        return JsonResponse({"error":"No user id", "details": "A user_id is required"}, status=400)

    game_manager.create_game([user_id, user_id], type="local1v1")
    return JsonResponse({"success": "Games created"})


@csrf_exempt
@require_http_methods(["POST"])
def can_join(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
    except:
        return JsonResponse({"error":"No user id", "details": "A user_id is required"}, status=400)
    
    try:
        data = json.loads(request.body)
        game_id = data.get("game_id")
    except:
        return JsonResponse({"error":"No game id", "details": "A game_id is required"}, status=400)

    game = PongGame.objects.filter(game_id=game_id)
    if not game.exists():
        return JsonResponse({"error":"No game with id", "details": "No game with this id found"}, status=400)
    
    game = game.get()
    if not user_id in [int(id) for id in game.users]:
        return JsonResponse({"error":"Cannot join game", "details": "Player cannot join this game"}, status=403)

    if game.status == "finished":
        return JsonResponse({"error":"Game ended", "details": "This game has ended"}, status=403)

    return JsonResponse({"success": "User can join the game"})

def run_start_game(game_id):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_in_executor(executor, lambda: loop.run_until_complete(game_manager.start_game(game_id)))