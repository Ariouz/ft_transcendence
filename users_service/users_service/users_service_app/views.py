from users_service_app.models import User
from django.http import JsonResponse
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
    url = "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-29f5277a5943e1f33349c04ecb3f211dc78d70e98943ad05d0f1328d38ba42f6&redirect_uri=http%3A%2F%2Flocalhost%3A8001%2Fapi%2Fauth%2F42%2Faccess&response_type=code"
    #todo request url
    return JsonResponse({"url":url})

# /auth/42/access/<code>
def ft_auth_access(request):
    code = request.GET.get("code", None)
    if code is None:
        return JsonResponse({"'code' parameter is expected"})
    data = get_access_token("authorization_code", code, "http://localhost:8001/api/auth/42/success", "https://api.intra.42.fr/oauth/token") # todo: fix error a this point
    return JsonResponse({"data":data}) # todo: data should be an access token

def ft_auth_success(request):
    return JsonResponse({"message":"Authentication success"})

def ft_auth_data(request, code):

    return JsonResponse({"received_code": code})
