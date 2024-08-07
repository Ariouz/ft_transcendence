from users_service_app.models import *
from django.http import JsonResponse
from .ft_api import get_access_token, get_user_data

# /auth/42
def ft_auth(request):
    url = "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-29f5277a5943e1f33349c04ecb3f211dc78d70e98943ad05d0f1328d38ba42f6&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fapi%2Fauth%2F42%2Faccess&response_type=code"
    return JsonResponse({"url":url})

# /auth/42/access?code=
def ft_auth_access(request):
    code = request.GET.get("code", None)
    if code is None:
        return JsonResponse({"error":"Failed to fetch access token","details":"A 'code' parameter is expected"})
    token_url = "https://api.intra.42.fr/oauth/token"
    redirect_url = "http://localhost:8080/api/auth/42/access"
    try:
        data = get_access_token("authorization_code", code, redirect_url, token_url)
        return data
    except Exception as e:
        return JsonResponse({"error":"Failed to fetch access token","details":str(e)})

# /auth/42/data/42/<access_token>/
def ft_auth_data_all(request, access_token):
    try:
        user_data = get_user_data(access_token, "https://api.intra.42.fr/v2/me")
        return user_data
    except Exception as e:
        return JsonResponse({"error":"Failed to fetch user data","details":str(e)})

# /auth/42/data/username/<access_token>/
def ft_auth_data_username(request, access_token):
    if (User.objects.filter(token=access_token).exists()):
        return JsonResponse({"username":User.objects.filter(token=access_token).get().username})
    return JsonResponse({"error":"User not found","details":"No user account exists with this token"})

# /auth/42/data/settings/<access_token>/
def ft_auth_data_settings(request, access_token):
    if (User.objects.filter(token=access_token).exists()):
        user = User.objects.filter(token=access_token).get()
        userSetting = UserSettings.objects.filter(user_id=user.user_id).get()
        data = {
            "user_id": user.user_id,
            "username": user.username,
            "full_name": user.fullname,
            "email": user.email,
            "avatar": f"http://localhost:8001{userSetting.avatar.url}",
            "display_name": userSetting.display_name,
            "lang": userSetting.lang,
            "github": userSetting.github,
            "status_message": userSetting.status_message
        }
        return JsonResponse(data)
    return JsonResponse({"error":"User not found","details":"No user account exists with this token"})


def ft_auth_data_confidentiality_settings(request, access_token):
    if (User.objects.filter(token=access_token).exists()):
        user = User.objects.filter(token=access_token).get()
        userConfidentiality = UserConfidentialitySettings.objects.get(user_id=user.user_id)
        data = {
            "profile_visibility": userConfidentiality.profile_visibility,
            "show_fullname": userConfidentiality.show_fullname,
            "show_email": userConfidentiality.show_email
        }
        return JsonResponse(data)
    return JsonResponse({"error":"User not found","details":"No user account exists with this token"})