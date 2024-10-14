from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from pong_service_app.models import *
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from concurrent.futures import ThreadPoolExecutor
import ft_requests
import redis
import json
import logging
from . import game_manager
import asyncio

executor = ThreadPoolExecutor(max_workers=5)

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
    
    logging.getLogger("django").info(f"Starting game")
    
    
    executor.submit(run_start_game, game_id)
    
    return JsonResponse({"success": "Games started"})

def run_start_game(game_id):
    asyncio.run(game_manager.start_game(game_id=game_id))