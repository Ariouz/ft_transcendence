from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from pong_service_app.models import *
from .. import pong_user
from pong_service_app.response_messages import success_response, error_response
import logging
import json

@require_http_methods(["POST"])
def delete_account(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        user = PongUser.objects.get(user_id=user_id)
    except Exception as e:
        return error_response(request, "user_not_found", "cannot_find_user_with_this_token", status_code=404)
    
    if not user:
        return success_response(request, "pong_user_not_created")

    stats = PongUserStats.objects.get(user_id=user_id)
    if stats:
        stats.delete()
    user.delete()
    return success_response(request, "account_successfully_deleted")
