from django.urls import path
from .views import LobbyView,LobbyGameView, LobbyUpdateView


urlpatterns = [
  path('', LobbyView.as_view(), name='lobby'),
  path('<int:lobby_id>/userId/<int:user_id>', LobbyUpdateView.as_view(), name='lobby-update')
]