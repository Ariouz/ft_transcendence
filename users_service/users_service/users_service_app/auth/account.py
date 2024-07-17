from users_service_app.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
import requests
import os
from .ft_api import get_access_token, get_user_data
from uuid import uuid4

def create_account(request):
    username = request.GET.get("username")
    email = request.GET.get("email")
    token = request.GET.get("token")
    if (User.objects.filter(username=username).exists()):
        return JsonResponse({"message":"Account already created"}, status=200)
    user = User.objects.create(username=username, email=email, token=token)
    return JsonResponse({"message":"Account successfully created", "user_id":user.id, "token":token}, status=200)

def account_exists(request):
    username = request.GET.get("username")
    if (User.objects.filter(username=username).exists()):
        return JsonResponse({"exists":True})
    return JsonResponse({"exists":False})