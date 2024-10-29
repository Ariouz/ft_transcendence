from django.urls import path
from .api import queue
from .api import game
from .api.data_endpoints import user_stats

urlpatterns = [
    path('queue/join/', queue.join_queue, name="join_queue"),
    path('queue/leave/', queue.leave_queue, name="leave_queue"),

    path('game/data/', game.get_game_data, name="get_game_data"), 
    path('game/create/local/', game.create_local_game, name="create_local_game"),
    path('game/start/', game.start_game, name="start_game"),

    path('game/can-join/', game.can_join, name="can_join"),

    path('user/game-history/<int:user_id>', user_stats.user_history, name="user_history"),

]