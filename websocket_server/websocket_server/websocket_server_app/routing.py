from django.urls import path
from .consumers import FriendsConsumer

websocket_urlpatterns = [
    path('ws/friends/<str:token>/', FriendsConsumer.as_asgi()),
]
