from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from pong_service_app.models import *
from concurrent.futures import ThreadPoolExecutor
import json
import logging
from . import game_manager
import asyncio
from pong_service_app.response_messages import success_response, error_response
from .themes import get_theme
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async

executor = ThreadPoolExecutor()

def create_game(players, type, tournament_id=None, theme=None):
    game = PongGame.objects.create(users=players, type=type, map_theme=get_theme(type) if not theme else get_theme(theme), tournament_id=tournament_id)
    game.save()
    channel_layer = get_channel_layer()

    logging.getLogger("django").info(f"Creating game with {players}")

    if type == "local1v1":
        players.pop() # double websocket

    for user_id in players:
        async_to_sync(channel_layer.group_send)(
            f"pong_user_{user_id}", {
                "type": "game_create",
                "game_id": game.game_id
            }
        )
    return game.game_id

@require_http_methods(["GET"])
def get_game_data(request):
    game_id = request.GET.get("game_id")

    if game_id is None:
        return error_response(request, "game_no_id", "game_id_required")

    if not PongGame.objects.filter(game_id=game_id).exists():
        return error_response(request, "game_not_found", "game_none_with_this_id_found")
    
    game = PongGame.objects.get(game_id=game_id)
    
    data = {
        "game_id": game_id,
        "players": game.users,
        "status": game.status,
        "type": game.type,
        "score": game.score,
        "winner_id": game.winner_id,
        "theme": game.map_theme,
        "is_tournament": game.tournament_id is not None
    }
    return success_response(request, "data_retrieved", extra_data={"data": data})

@csrf_exempt
@require_http_methods(["POST"])
def start_game(request):

    logging.getLogger("django").info(f"Received start request")
    try:
        data = json.loads(request.body)
        game_id = data.get("game_id")
    except:
        return error_response(request, "game_no_id", "game_id_required")

    if not PongGame.objects.filter(game_id=game_id).exists():
        logging.getLogger("django").info(f"Game not found {game_id}")
        return error_response(request, "game_not_found", "game_none_with_this_id_found")
    
    logging.getLogger("django").info(f"Starting game {game_id}")
    run_start_game(game_id)
    
    return success_response(request, "game_started")


@require_http_methods(["POST"])
def create_local_game(request):

    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
    except:
        return error_response(request, "user_no_id", "user_id_required")

    game_manager.create_game([user_id, user_id], type="local1v1")
    return success_response(request, "game_created")


@require_http_methods(["POST"])
def can_join(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
    except:
        return error_response(request, "user_no_id", "user_id_required")
    
    try:
        data = json.loads(request.body)
        game_id = data.get("game_id")
    except:
        return error_response(request, "game_no_id", "game_id_required")

    game = PongGame.objects.filter(game_id=game_id)
    if not game.exists():
        return error_response(request, "game_none_with_id", "game_none_with_this_id_found")
    
    game = game.get()
    if not user_id in [int(id) for id in game.users]:
        return error_response(request, "game_cannot_join", "player_cannot_join_this_game", status=403)

    if game.status in ["finished", "forfaited"]:
        return error_response(request, "game_ended", "game_has_ended", status=403)

    return success_response(request, "game_user_can_join", extra_data={"success":True})

def run_start_game(game_id):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_in_executor(executor, lambda: loop.run_until_complete(game_manager.start_game(game_id)))