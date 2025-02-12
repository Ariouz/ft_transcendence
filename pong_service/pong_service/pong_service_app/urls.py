from django.urls import path
from .api import queue
from .api import game
from .api.data_endpoints import user_stats, leaderboard
from .tournaments import tournament_endpoints, tournament_rounds
from .csrf_protection import get_csrf_token

urlpatterns = [
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),


    # Pong
    path('queue/join/', queue.join_queue, name="join_queue"),
    path('queue/leave/', queue.leave_queue, name="leave_queue"),

    path('game/data/', game.get_game_data, name="get_game_data"), 
    path('game/create/local/', game.create_local_game, name="create_local_game"),
    path('game/start/', game.start_game, name="start_game"),
    path('game/start-local/', game.start_local_game, name="start_local_game"),

    path('game/can-join/', game.can_join, name="can_join"),

    # Pong stats
    path('user/game-history/<int:user_id>', user_stats.user_history, name="user_history"),
    path('user/stats/<int:user_id>', user_stats.get_user_stats, name="get_user_stats"),

    path('all/leaderboard/', leaderboard.get_leaderboard, name="get_leaderboard"),

    
    # Tournaments
    path('tournament/create/', tournament_endpoints.create_tournament, name="create_tournament"),
    path('tournament/delete/', tournament_endpoints.delete_tournament, name="delete_tournament"),

    path('tournament/launch/', tournament_rounds.launch_tournament, name="launch_tournament"),
    path('tournament/get-rounds/', tournament_rounds.get_tournament_rounds, name="get_tournament_rounds"),
    path('tournament/start-round/', tournament_rounds.start_next_tournament_round, name="start_next_tournament_round"),
    

    path('tournament/join/', tournament_endpoints.join_tournament, name="join_tournament"),
    path('tournament/leave/', tournament_endpoints.leave_tournament, name="leave_tournament"),
    path('tournament/ws-connect/', tournament_endpoints.ws_connect, name="ws_connect"),

    path('tournament/does-participates/', tournament_endpoints.does_participates, name="does_participates"),
    path('tournament/get-hosted/', tournament_endpoints.get_hosted_tournament, name="get_hosted_tournament"),
    path('tournament/is-host/', tournament_endpoints.is_host, name="is_host"),
    path('tournament/state/', tournament_endpoints.tournament_state, name="tournament_state"),
    path('tournament/list/', tournament_endpoints.tournament_list, name="tournament_list"),
    path('tournament/participants/', tournament_endpoints.tournament_participants, name="tournament_participants"),
    

]