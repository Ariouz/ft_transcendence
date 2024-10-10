from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from pong_service_app.models import *
import game_endpoints
import ft_requests
import redis
import json

redis_client = redis.StrictRedis(host="redis-websocket-users", port="6379", db=0)
redis_pong_1_1_queue = "pong-1v1-queue"

def is_user_in_queue(user_id):
    return redis_client.exists(redis_pong_1_1_queue, user_id)

def check_queue_size():
    if redis_client.llen(redis_pong_1_1_queue) >= 2:
        users = []
        users.append(redis_client.rpop(redis_pong_1_1_queue, 2))
        game_endpoints.create_game(users)


@csrf_exempt
@require_http_methods(["POST"])
def join_queue(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
    except:
        return JsonResponse({"error":"Invalid JSON", "details":"Invalid JSON"}) # TODO change to error_response

    if user_id is None:
        return JsonResponse({"error":"User Id required", "details":"user_id field is required"}) # TODO change to error_response
    
    if is_user_in_queue(user_id):
        return JsonResponse({"error":"Already in queue", "details":"User is already in the queue"}) # TODO change to error_response
    
    redis_client.lpush(redis_pong_1_1_queue, user_id)
    check_queue_size()
    return JsonResponse({"success":"Successfully joined the queue!"}) # TODO change to success_response


@csrf_exempt
@require_http_methods(["POST"])
def leave_queue(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
    except:
        return JsonResponse({"error":"Invalid JSON", "details":"Invalid JSON"}) # TODO change to error_response

    if user_id is None:
        return JsonResponse({"error":"User Id required", "details":"user_id field is required"}) # TODO change to error_response

    if not is_user_in_queue(user_id):
        return JsonResponse({"error":"Not in queue", "details":"User is not in the queue"}) # TODO change to error_response
    
    redis_client.lrem(redis_pong_1_1_queue, 0, user_id)
    return JsonResponse({"success":"Successfully leaved the queue!"}) # TODO change to success_response
