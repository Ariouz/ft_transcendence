import redis
from django.http import JsonResponse

redis_client = redis.StrictRedis(host="redis-websocket-users", port="6379", db=0)

def get_user_status(request, user_id):
    return JsonResponse({"status": redis_client.exists(f"user-{user_id}-online")})