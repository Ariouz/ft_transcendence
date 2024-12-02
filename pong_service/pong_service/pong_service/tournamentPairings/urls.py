from django.urls import path
from .views import CreateMatchMakingView, UpdateWinnerView, FilterView


urlpatterns = [
  path('createMatchMaking/<int:id>/roundId/<int:roundId>', CreateMatchMakingView.as_view(), name='create-matchMaking'),
  path('winner/', UpdateWinnerView.as_view(), name='Update-Winner'),
  path('<str:UDID>', FilterView.as_view(), name='get-tournament'),
]