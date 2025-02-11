from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from pong_service_app.models import *
from .. import pong_user
from pong_service_app.response_messages import success_response, error_response

@require_http_methods(["GET"])
def user_history(request, user_id):
    offset = int(request.GET.get("offset", 0))
    limit = int(request.GET.get("limit", 50))

    if not PongUser.objects.filter(user_id=user_id).exists():
        return error_response(request, "user_not_found", "user_not_found_id", status_code=404)
    
    user = PongUser.objects.filter(user_id=user_id).get()
    history = user.game_history

    offset = max(0, offset)
    limit = max(1, limit)

    if offset >= len(history):
            return success_response(request, "history_found", extra_data={"user_id": user_id, "history": {}})
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

    return success_response(request, "history_found", extra_data={"user_id": user_id, "history": games, "online_games_played": game_count})

def get_user_stats(request, user_id):
    user_stats = pong_user.get_user_stats(user_id)

    stats = {
        "played": user_stats.played,
        "wins": user_stats.wins,
        "loses": user_stats.loses,
        "ratio": pong_user.get_win_rate(user_id)
    }
    return success_response(request, "data_retrieved", extra_data={"data": stats})