from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from pong_service_app.models import *
import ft_requests
import redis
import json

# Not an endpoint, only used by self-service
def create_game(players):
    game = PongGame.objects.create(users=players)
    game.save()
    channel_layer = get_channel_layer()
    for user_id in players:
        async_to_sync(channel_layer.group_send)(
            f"pong_user_{user_id}", {
                "type": "game_create",
                "game_id": game.game_id
            }
        )