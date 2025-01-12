from django.views.decorators.http import require_http_methods
from pong_service_app.models import *
import redis
import json
from . import game_manager
import logging
from . import pong_user
from pong_service_app.response_messages import success_response, error_response

redis_client = redis.StrictRedis(host="redis-websocket-users", port="6379", db=0)
redis_pong_1_1_queue = "pong-1v1-queue"
redis_pong_arcade_queue = "pong-arcade-queue"

def is_user_in_queue(user_id, game_type):
    redis_queue = get_redis_queue(game_type)
    queue = redis_client.lrange(redis_queue, 0, -1)
    decode_queue = [uid.decode("utf-8") for uid in queue]
    logging.getLogger("django").info(f"matchmaking, of {game_type}, queue: {decode_queue}")
    logging.getLogger("django").info(f"is {user_id} in {decode_queue}: {str(user_id) in decode_queue}")
    return str(user_id) in decode_queue

def check_queue_size(game_type):
    redis_queue = get_redis_queue(game_type)
    if redis_client.llen(redis_queue) >= 2:
        users = []
        users.append(redis_client.rpop(redis_queue).decode("utf-8"))
        users.append(redis_client.rpop(redis_queue).decode("utf-8"))
        game_manager.create_game(users, type=game_type)


def get_redis_queue(game_type):
    return redis_pong_arcade_queue if game_type == "arcade" else redis_pong_1_1_queue


@require_http_methods(["POST"])
def join_queue(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        game_type = data.get("game_type")
    except:
        return error_response(request, "invalid_json", "invalid_json")

    if user_id is None:
        return error_response(request, "user_no_id", "user_id_required")
    
    if is_user_in_queue(user_id, game_type):
        return error_response(request, "Already in queue", "User is already in the queue")
    
    game_types = ["1v1", "arcade"]
    if not game_type in game_types:
        return error_response(request, "game_type_invalid", "game_type_invalid")

    pong_user.create_user_if_not_exists(user_id)

    redis_queue = get_redis_queue(game_type)
    redis_client.lpush(redis_queue, user_id)
    check_queue_size(game_type)
    return success_response(request, "queue_successfully_joined")


@require_http_methods(["POST"])
def leave_queue(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        game_type = data.get("game_type")
    except:
        return error_response(request, "invalid_json", "invalid_json")

    if user_id is None:
        return error_response(request, "user_no_id", "user_id_required")
    
    game_types = ["1v1", "arcade"]
    if not game_type in game_types:
        return error_response(request, "game_type_invalid", "game_type_invalid")

    if not is_user_in_queue(user_id, game_type):
        return error_response(request, "not_in_queue", "queue_user_is_not_in")
    
    redis_queue = get_redis_queue(game_type)
    redis_client.lrem(redis_queue, 0, user_id)
    return success_response(request, "queue_successfully_left")
