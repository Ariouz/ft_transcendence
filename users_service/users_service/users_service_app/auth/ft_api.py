from django.http import JsonResponse
from ft_requests import ftrequests
import os
import logging

def get_access_token(grantType, code=None, redirect=None, url="https://api.intra.42.fr/v2/oauth/token"):
    UID = os.getenv("API_42_UID")
    SECRET = os.getenv("API_42_SECRET")

    payload = {
        "grant_type": grantType,
        "client_id": UID,
        "client_secret": SECRET,
        "code": code,
        "redirect_uri": redirect
    }
    response = ftrequests.post(url, data=payload)
    
    logger = logging.getLogger("users_logger")
    logger.info('response: %s', response)
    logger.info('response.status_code: %s', response.status_code)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        raise Exception(response)

def get_user_data(access_token, url):
    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }

    response = ftrequests.get(url, headers=headers)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        raise Exception(response)