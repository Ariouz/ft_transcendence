from users_service_app.models import *
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from .ft_api import get_access_token, get_user_data
from uuid import uuid4
from ft_requests import ftrequests
import os

def create_account(request):
    username = request.GET.get("username")
    email = request.GET.get("email")
    token = request.GET.get("token")
    fullname = request.GET.get("fullname")

    if (User.objects.filter(username=username).exists()):
        if (User.objects.filter(token=token).exists()):
            return JsonResponse({"message":"Account already created"}, status=200)
        else:
            user = User.objects.get(username=username)
            user.token = token
            user.save()
            return JsonResponse({"message":"Account token successfully updated", "user_id":user.user_id, "token":token}, status=200)
    
    user = User.objects.create(username=username, email=email, token=token, fullname=fullname)
    userSettings = UserSettings.objects.create(user_id=user.user_id, display_name=username)
    UserConfidentialitySettings.objects.create(user_id=user.user_id)

    avatar = request.GET.get("avatar")
    try:
        response = ftrequests.get(avatar)
        if response.status_code == 200:
            avatar_content = ContentFile(response.content)
            avatar_name =f'/user_{user.user_id}.jpg'
            userSettings.avatar.save(avatar_name, avatar_content)
            userSettings.save()
    except UserSettings.DoesNotExist:
        return JsonResponse({"error":"Failed to create account", "details":"Cannot fetch user default avatar"})

    return JsonResponse({"message":"Account successfully created", "user_id":user.user_id, "token":token}, status=200)

def account_exists(request):
    username = request.GET.get("username")
    token = request.GET.get("token")

    return JsonResponse({  "exists": User.objects.filter(username=username, token=token).exists() })
