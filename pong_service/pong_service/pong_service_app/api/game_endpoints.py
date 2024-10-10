from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from pong_service_app.models import *
import ft_requests
import redis
import json

# Not an endpoint, only used by self-service
def create_game(players):
    game = PongGame.objects.create(users=players)
    game.save()
    # TODO send websocket to users to navigate to game