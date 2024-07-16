from django.urls import path

from .views import users, ft_auth, ft_auth_access, ft_auth_success

urlpatterns = [
    path('users/', users, name="users"),
    # path('auth/', auth, name="auth"),
    path('auth/42/', ft_auth, name="ft_auth"),
    path('auth/42/access/', ft_auth_access, name="ft_auth_access"),
    path('auth/42/success/', ft_auth_success, name="ft_auth_success"),
    # path('auth/42/data/<str:code>/', ft_auth_data, name="ft_auth_data"),
]

