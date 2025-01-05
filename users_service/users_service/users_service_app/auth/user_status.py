import redis
from django.http import JsonResponse
from users_service_app.response_messages import json_response

redis_client = redis.StrictRedis(host="redis-websocket-users", port="6379", db=0)

def get_user_status(request, user_id):
    return json_response({"status": redis_client.exists(f"user-{user_id}-online")})