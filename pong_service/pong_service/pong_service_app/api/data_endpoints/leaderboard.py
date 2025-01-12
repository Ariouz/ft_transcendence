from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import F
from pong_service_app.models import *
from .. import pong_user
from pong_service_app.response_messages import success_response

@require_http_methods(["GET"])
def get_leaderboard(request):
    offset = int(request.GET.get("offset", 0))
    limit = int(request.GET.get("limit", 50))

    offset = max(0, offset)
    limit = max(1, limit)

    leaderboard = (PongUserStats.objects
        .exclude(played=0)
        .annotate(
            ratio=F('wins') * 100.0 / (F('played') + 1),
            score=F('wins') + F('played') * 0.1
        )
        .order_by('-score', '-ratio', '-wins'))

    if offset >= len(leaderboard):
            return success_response(request, "leaderboard_found", extra_data={"leaderboard": {}})
    if offset > len(leaderboard):
        offset = len(leaderboard)

    users = {}
    count = 0

    paginator = Paginator(leaderboard, limit)
    page_number = offset // limit + 1
    page = paginator.get_page(page_number)

    for rank, u in enumerate(page.object_list, start=1):
        if count >= limit: break

        stat = u
        user_id = stat.user_id

        user_rank = (page_number - 1) * limit + rank
        
        users[user_id] = {
            "rank": user_rank,
            "user_id": user_id,
            "played": stat.played,
            "wins": stat.wins,
            "loses": stat.loses,
            "win_rate": 0 if stat.wins <= 0 else round(stat.wins / stat.played, 2) * 100
        }
        
        count += 1

    user_count = PongUserStats.objects.exclude(played=0).count()
    return success_response(request, "leaderboard_found", extra_data={"leaderboard": users, "user_count": user_count})