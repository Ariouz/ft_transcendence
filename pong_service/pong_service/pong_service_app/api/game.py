from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from pong_service_app.models import *
import ft_requests
import redis
import json
from . import game_endpoints


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