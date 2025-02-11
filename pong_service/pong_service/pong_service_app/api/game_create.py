from pong_service_app.models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from .themes import get_theme
import logging

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