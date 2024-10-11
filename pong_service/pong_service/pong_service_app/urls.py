from django.urls import path
from .api import queue
from .api import game

urlpatterns = [
    path('queue/join/', queue.join_queue, name="join_queue"),
    path('queue/leave/', queue.leave_queue, name="leave_queue"),

    path('game/data/', game.get_game_data, name="get_game_data"),

]