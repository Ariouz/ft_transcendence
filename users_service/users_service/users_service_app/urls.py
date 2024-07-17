from django.urls import path

from .views import users, ft_auth, ft_auth_access, ft_auth_data

urlpatterns = [
    path('users/', users, name="users"),
    # path('auth/', auth, name="auth"),
    path('auth/42/', ft_auth, name="ft_auth"),
    path('auth/42/access/', ft_auth_access, name="ft_auth_access"),
    path('auth/42/data/<str:access_token>/', ft_auth_data, name="ft_auth_data"),
    # path('auth/42/data/<str:code>/', ft_auth_data, name="ft_auth_data"),
]

