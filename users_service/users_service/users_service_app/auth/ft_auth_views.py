from users_service_app.models import *
from .ft_api import get_access_token, get_user_data
from django.views.decorators.http import require_http_methods
import urllib.parse
import os
from users_service_app.response_messages import error_response, json_response
from django.contrib.auth.hashers import make_password
import logging


host = os.getenv("HOST_IP")

# /auth/42/
def ft_auth(request):
    encoded_host = urllib.parse.quote(host)
    UID = os.getenv("API_42_UID")
    url = f"https://api.intra.42.fr/oauth/authorize?client_id={UID}&redirect_uri=https%3A%2F%2F{encoded_host}%3A8443%2Fapi%2Fauth%2F42%2Faccess&response_type=code"
    return json_response({"url":url})

# /auth/42/access/?code=
@require_http_methods(["GET"])
def ft_auth_access(request):
    code = request.GET.get("code", None)
    if code is None:
        return error_response(request, "failed_to_fetch_access_token", "a_code_parameter_is_expected")
    token_url = "https://api.intra.42.fr/oauth/token"
    redirect_url = f"https://{host}:8443/api/auth/42/access"
    try:
        token_data = get_access_token("authorization_code", code, redirect_url, token_url)
        token = token_data['access_token']

        user_data = get_user_data(token, "https://api.intra.42.fr/v2/me")

        data = {
            "access_token": make_password(token),
            "expires_in": token_data['expires_in'],
            "login": user_data['login'],
            "email": user_data['email'],
            "image": user_data['image']['link'],
            "usual_full_name": user_data["usual_full_name"]
            }
        
        return json_response(data)
    except Exception as e:
        return error_response(request, "failed_to_fetch_access_token", str(e))


# UNUSED ???

# /auth/42/data/42/<access_token>/
def ft_auth_data_all(request, access_token):
    try:
        user_data = get_user_data(access_token, "https://api.intra.42.fr/v2/me")
        return user_data
    except Exception as e:
        return error_response(request, "failed_to_fetch_user_data", str(e))


# /auth/42/data/username/<access_token>/
def ft_auth_data_username(request, access_token):
    if (User.objects.filter(token=access_token).exists()):
        return json_response({"username":User.objects.filter(token=access_token).get().username})
    return error_response(request, "user_not_found", "account_no_user_with_token", status_code=404)

# /auth/42/data/id/<access_token>/
def ft_auth_data_id(request, access_token):
    if (User.objects.filter(token=access_token).exists()):
        return json_response({"user_id":User.objects.filter(token=access_token).get().user_id})
    return error_response(request, "user_not_found", "account_no_user_with_token", status_code=404)


# /auth/42/data/settings/<access_token>/<host>
def ft_auth_data_settings(request, access_token):
    if (User.objects.filter(token=access_token).exists()):
        user = User.objects.filter(token=access_token).get()
        userSetting = UserSettings.objects.filter(user_id=user.user_id).get()
        
        avatar_url = (
            f"https://{host}:8001{userSetting.avatar.url}" if userSetting.avatar else None
        )
        
        data = {
            "user_id": user.user_id,
            "username": user.username,
            "full_name": user.fullname,
            "email": user.email,
            "avatar": avatar_url,
            "display_name": userSetting.display_name,
            "lang": userSetting.lang,
            "github": userSetting.github,
            "status_message": userSetting.status_message
        }
        return json_response(data)
    return error_response(request, "user_not_found", "account_no_user_with_token", status_code=404)

# /account/settings/confidentiality/<str:access_token>/
def ft_auth_data_confidentiality_settings(request, access_token):
    if (User.objects.filter(token=access_token).exists()):
        user = User.objects.filter(token=access_token).get()
        userConfidentiality = UserConfidentialitySettings.objects.get(user_id=user.user_id)
        data = {
            "profile_visibility": userConfidentiality.profile_visibility,
            "show_fullname": userConfidentiality.show_fullname,
            "show_email": userConfidentiality.show_email
        }
        return json_response(data)
    return error_response(request, "user_not_found", "account_no_user_with_token", status_code=404)

# /user/profile/data/<int:user_id>/
def get_profile_data_id(request, user_id):
    if (User.objects.filter(user_id=user_id).exists()):
        return get_profile_data_username(request, User.objects.filter(user_id=user_id).get().username)
    return error_response(request, "user_not_found", "account_no_user_with_id", status_code=404)

# /user/profile/data/<str:username>/
def get_profile_data_username(request, username):

    if not User.objects.filter(username=username).exists():
        return error_response(request, "user_not_found", "cannot_find_user_with_this_username", status_code=404)

    user = User.objects.get(username=username)
    userConfidentiality = UserConfidentialitySettings.objects.get(user_id=user.user_id)
    userSetting = UserSettings.objects.get(user_id=user.user_id)

    data = {
            "user_id": user.user_id,
            "username": user.username,
            "full_name": user.fullname,
            "email": user.email,
            "avatar": f"https://{host}:8001{userSetting.avatar.url}",
            "display_name": userSetting.display_name,
            "lang": userSetting.lang,
            "github": userSetting.github,
            "status_message": userSetting.status_message,
        }

    if userConfidentiality.profile_visibility == "private":
        data["full_name"] = "Hidden"
        data["email"] = "Hidden"
        data["status_message"] = "Hidden"
        data["github"] = "null"
    
    if userConfidentiality.show_fullname == False:
        data["full_name"] = "Hidden"
    
    if userConfidentiality.show_email == False:
        data["email"] = "Hidden"

    return json_response(data)


# /users/all/data/
def get_all_users_data(request):
    data = {}
    for user in User.objects.all():
        userSettings = UserSettings.objects.get(user_id=user.user_id)
        userData = {}
        userData["username"] = user.username
        userData["avatar"] = f"https://{host}:8001{userSettings.avatar.url}"
        data[user.user_id] = userData
    return json_response(data)


# /auth/42/data/displayname/<user_id>/
def ft_auth_data_displayname(request, user_id):
    if (UserSettings.objects.filter(user_id=user_id).exists()):
        return json_response({"display_name":UserSettings.objects.filter(user_id=user_id).get().display_name})
    return error_response(request, "user_not_found", "account_no_user_with_id", status_code=404)
