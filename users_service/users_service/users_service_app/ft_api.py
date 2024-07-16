from django.http import JsonResponse
import requests

def get_access_token(grantType, code=None, redirect=None, url="https://api.intra.42.fr/v2/oauth/token"):
    UID = "u-s4t2ud-29f5277a5943e1f33349c04ecb3f211dc78d70e98943ad05d0f1328d38ba42f6"
    SECRET = "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"
    payload = {
        "grant_type": grantType,
        "client_id": UID,
        "client_secret": SECRET,
        "code": code,
        "redirect_uri": redirect
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        raise Exception(response.json())