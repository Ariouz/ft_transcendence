from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from pong_service_app.models import *
import ft_requests
import redis
import json
from . import game_manager
import logging

redis_client = redis.StrictRedis(host="redis-websocket-users", port="6379", db=0)
redis_pong_1_1_queue = "pong-1v1-queue"

def is_user_in_queue(user_id):
    queue = redis_client.lrange(redis_pong_1_1_queue, 0, -1)
    decode_queue = [uid.decode("utf-8") for uid in queue]
    logging.getLogger("django").info(f"matchmaking queue: {decode_queue}")
    logging.getLogger("django").info(f"is {user_id} in {decode_queue}: {str(user_id) in decode_queue}")
    return str(user_id) in decode_queue

def check_queue_size():
    if redis_client.llen(redis_pong_1_1_queue) >= 2:
        users = []
        users.append(redis_client.rpop(redis_pong_1_1_queue).decode("utf-8"))
        users.append(redis_client.rpop(redis_pong_1_1_queue).decode("utf-8"))
        game_manager.create_game(users, type="1v1")


@csrf_exempt
@require_http_methods(["POST"])
def join_queue(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
    except:
        return JsonResponse({"error":"Invalid JSON", "details":"Invalid JSON"})

    if user_id is None:
        return JsonResponse({"error":"User Id required", "details":"user_id field is required"})
    
    if is_user_in_queue(user_id):
        return JsonResponse({"error":"Already in queue", "details":"User is already in the queue"})
    
    redis_client.lpush(redis_pong_1_1_queue, user_id)
    check_queue_size()
    return JsonResponse({"success":"Successfully joined the queue!"})


@csrf_exempt
@require_http_methods(["POST"])
def leave_queue(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
    except:
        return JsonResponse({"error":"Invalid JSON", "details":"Invalid JSON"})

    if user_id is None:
        return JsonResponse({"error":"User Id required", "details":"user_id field is required"})

    if not is_user_in_queue(user_id):
        return JsonResponse({"error":"Not in queue", "details":"User is not in the queue"})
    
    redis_client.lrem(redis_pong_1_1_queue, 0, user_id)
    return JsonResponse({"success":"Successfully left the queue!"})
