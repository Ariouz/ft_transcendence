import redis

redis_client = redis.StrictRedis(host="redis-websocket-users", port="6379", db=0)

def set_user_online(user_id):
        redis_client.set(f"user-{user_id}-online", 1)

def set_user_offline(user_id):
        redis_client.delete(f"user-{user_id}-online")
