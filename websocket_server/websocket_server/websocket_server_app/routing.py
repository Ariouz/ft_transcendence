from django.urls import path
from .user_ws.consumers import FriendsConsumer
from .pong_ws.game_consumer import PongGameConsumer
from .pong_ws.user_consumer import PongUserConsumer
from .tournaments.user_consumer import TournamentUserConsumer
from .tournaments.tournament_consumer import TournamentConsumer

websocket_urlpatterns = [
    # User
    path('ws/friends/<str:token>/', FriendsConsumer.as_asgi()),

    # Pong
    path('ws/pong/user/<str:token>/', PongUserConsumer.as_asgi()),
    path('ws/pong/game/<str:token>/<int:game_id>/', PongGameConsumer.as_asgi()),

    # Pong tournaments
    path('ws/tournament/user/<str:token>/', TournamentUserConsumer.as_asgi()),
    path('ws/tournament/tournament/<str:token>/<int:tournament_id>/', TournamentConsumer.as_asgi()),
]
