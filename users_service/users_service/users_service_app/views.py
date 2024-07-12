from users_service_app.models import User
from django.http import JsonResponse
import requests
import os
import logging

logger = logging.getLogger(__name__)

# /'users/'
def users(request):
    users_list = User.objects.all()
    users_list = list(users_list.values())
    context = {
        "users": users_list,
    }

    return JsonResponse(context)

def auth(request):
    UID = "u-s4t2ud-29f5277a5943e1f33349c04ecb3f211dc78d70e98943ad05d0f1328d38ba42f6"
    SECRET = "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"
    url = "https://api.intra.42.fr/v2/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": UID,
        "client_secret": SECRET
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({'error': 'Failed to fetch token', 'details': response.json()}, status=response.status_code)

