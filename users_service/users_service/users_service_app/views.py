from users_service_app.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
import requests
import os
from .ft_api import get_access_token

# /'users/'
def users(request):
    users_list = User.objects.all()
    users_list = list(users_list.values())
    context = {
        "users": users_list,
    }

    return JsonResponse(context)

# /auth/42
def ft_auth(request): #redirect -> localhost:8001/auth/42/access/<code>
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

def ft_auth_success(request):
    return JsonResponse({"message":"Authentication success"})

def ft_auth_data(request, code):

    return JsonResponse({"received_code": code})
    #f9de805b9fc3157dd05ab4c3e125f25e78fa989a57013a42dc8c4311a97894d0
