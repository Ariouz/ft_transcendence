from django.urls import path
from .user_ws.consumers import FriendsConsumer
from .pong_ws.game_consumer import PongGameConsumer
from .pong_ws.user_consumer import PongUserConsumer

websocket_urlpatterns = [
    path('ws/friends/<str:token>/', FriendsConsumer.as_asgi()),
    path('ws/pong/user/<str:token>/', PongUserConsumer.as_asgi()),
    path('ws/pong/game/<str:token>/<int:game_id>/', PongGameConsumer.as_asgi()),
]
