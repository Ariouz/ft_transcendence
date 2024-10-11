from django.urls import path
from .user_ws.consumers import FriendsConsumer
from .pong_ws.consumers import PongConsumer

websocket_urlpatterns = [
    path('ws/friends/<str:token>/', FriendsConsumer.as_asgi()),
    path('ws/pong/<str:token>/', PongConsumer.as_asgi()),
]
