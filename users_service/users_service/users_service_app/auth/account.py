from users_service_app.models import *
from django.http import JsonResponse
from django.core.files.base import ContentFile
import ft_requests
from django.views.decorators.http import require_http_methods
from users_service_app.response_messages import error_response, success_response, json_response

@require_http_methods(["GET"])
def create_account(request):
    username = request.GET.get("username")
    email = request.GET.get("email")
    token = request.GET.get("token")
    fullname = request.GET.get("fullname")

    if (User.objects.filter(username=username).exists()):
        if (User.objects.filter(token=token).exists()):
            return success_response(request, "account_already_created")
        else:
            user = User.objects.get(username=username)
            user.token = token
            user.save()
            return success_response(request, "account_token_successfully_updated", extra_data={ "user_id": user.user_id, "token": token })
    
    user = User.objects.create(username=username, email=email, token=token, fullname=fullname)
    userSettings = UserSettings.objects.create(user_id=user.user_id, display_name=username)
    UserConfidentialitySettings.objects.create(user_id=user.user_id)

    avatar = request.GET.get("avatar")
    try:
        response = ft_requests.get(avatar)
        if response.status_code == 200:
            avatar_content = ContentFile(response.data)
            avatar_name =f'/user_{user.user_id}.jpg'
            userSettings.avatar.save(avatar_name, avatar_content)
            userSettings.save()
    except UserSettings.DoesNotExist:
        return error_response(request, "account_failed_to_create", "account_cannot_fetch_user_default_avatar")

    return success_response(request, "account_successfully_created", extra_data={ "user_id": user.user_id, "token": token })

@require_http_methods(["GET"])
def account_exists(request):
    username = request.GET.get("username")
    token = request.GET.get("token")

    return json_response({  "exists": User.objects.filter(username=username, token=token).exists() })
