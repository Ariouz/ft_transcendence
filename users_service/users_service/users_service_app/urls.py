from django.urls import path

from .views import users
from .auth.ft_auth_views import *
from .auth.account import create_account, account_exists
from .auth.account_settings import update_profile_settings, update_confidentiality_settings, delete_account
from .friends.friends_views import authenticate_user, list_friends, add_friend, remove_friend, is_following
from .auth.user_status import *

urlpatterns = [
    # path('users/', users, name="users"),

    # Auth
    path('auth/42/', ft_auth, name="ft_auth"),
    path('auth/42/access/', ft_auth_access, name="ft_auth_access"),

    # User data
    path('auth/42/data/42/<str:access_token>/', ft_auth_data_all, name="ft_auth_data_all"),
    path('auth/42/data/username/<str:access_token>/', ft_auth_data_username, name="ft_auth_data_username"),
    path('auth/42/data/id/<str:access_token>/', ft_auth_data_id, name="ft_auth_data_id"),
    path('auth/42/data/settings/<str:access_token>/', ft_auth_data_settings, name="ft_auth_data_settings"),
    path('auth/42/data/settings/confidentiality/<str:access_token>/', ft_auth_data_confidentiality_settings, name="ft_auth_data_confidentiality_settings"),
    
    # Account management
    path('account/create/', create_account, name="create_account"),
    path('account/exists/', account_exists, name="account_exists"),

    # User Settings
    path('account/settings/profile/<str:access_token>', update_profile_settings, name="update_profile_settings"),
    path('account/settings/confidentiality/<str:access_token>', update_confidentiality_settings, name="update_confidentiality_settings"),
    path('account/settings/delete/<str:access_token>', delete_account, name="delete_account"),

    # View other profile
    path('user/profile/data/<str:username>/', get_profile_data_username, name="get_profile_data_username"),
    path('users/all/data/', get_all_users_data, name="get_all_users_data"),

    # User status
    path('user/online-status/get/<int:user_id>/', get_user_status, name="get_user_status"),
    # path('user/online-status/online/<int:user_id>/', set_user_online, name="set_user_online"),
    # path('user/online-status/offline/<int:user_id>/', set_user_offline, name="set_user_offline"),

    # Friends
    path('user/authenticate/<str:token>/', authenticate_user, name='authenticate_user'),
    path('user/friends/<int:user_id>/', list_friends, name='list_friends'),
    path('user/friends/follows/<int:user_id>/<int:friend_id>/', is_following, name='is_following'),
    path('user/friends/<int:user_id>/add/<int:friend_id>/', add_friend, name='add_friend'),
    path('user/friends/<int:user_id>/remove/<int:friend_id>/', remove_friend, name='remove_friend'),
]


