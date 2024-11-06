from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from pong_service_app.models import *
from .. import pong_user

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
    if offset > len(history):
        offset = len(history)

    games = {}
    count = 0

    ponggames = PongGame.objects.filter(
        users__contains=str(user_id),
    ).exclude(type="local1v1").order_by('-game_id')

    paginator = Paginator(ponggames, limit)
    page = paginator.get_page(offset // limit + 1)

    for g in page.object_list:
        if count >= limit: break

        game = g
        game_id = g.game_id
        
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

def get_user_stats(request, user_id):
    user_stats = pong_user.get_user_stats(user_id)

    stats = {
        "played": user_stats.played,
        "wins": user_stats.wins,
        "loses": user_stats.loses,
        "ratio": pong_user.get_win_rate(user_id)
    }
    return JsonResponse({"success":"Data retrieved", "data": stats}, status=200)