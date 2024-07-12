from django.urls import path

from .views import users, auth

urlpatterns = [
    path('users/', users, name="users"),
    path('auth/', auth, name="auth"),
]
