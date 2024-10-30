from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from pong_service_app.models import *

@csrf_exempt
@require_http_methods(["GET"])
def user_history(request, user_id):
    offset = int(request.GET.get("offset", 0))
    limit = int(request.GET.get("limit", 50))

    if not PongUser.objects.filter(user_id=user_id).exists():
        return JsonResponse({"error":"User not found", "details": "No user found matching id"}, status=400)
    
    user = PongUser.objects.filter(user_id=user_id).get()
    history = user.game_history

    offset = max(0, offset)
    limit = max(0, limit)

    if offset >= len(history):
            return JsonResponse({"success":"History found", "user_id": user_id, "history": {}})
    if offset + limit > len(history):
        limit = len(history) - offset

    games = {}
    count = 0
    for i in range(offset, len(history)):
        if count >= limit: break

        game_id = history[i]
        game = PongGame.objects.filter(game_id=game_id).first()
        
        if not game or game.type == "local1v1":
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
        
        count += 1

    game_count = PongGame.objects.filter(
        users__contains=str(user_id),
    ).exclude(type="local1v1").count()

    return JsonResponse({"success":"History found", "user_id": user_id, "history": games, "online_games_played": game_count})

    