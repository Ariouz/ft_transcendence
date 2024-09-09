from users_service_app.models import User, Friend
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.views.decorators.csrf import csrf_exempt


@require_http_methods(["GET"])
def list_friends(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    friends = user.friends.all()
    friend_list = [
        {"user_id": friend.friend.user_id, "username": friend.friend.username}
        for friend in friends
    ]
    return JsonResponse({"friends": friend_list})


@csrf_exempt
@require_http_methods(["POST"])
def add_friend(request, user_id, friend_id):
    user = get_object_or_404(User, pk=user_id)
    friend = get_object_or_404(User, pk=friend_id)
    Friend.objects.create(user=user, friend=friend)
    send_friend_update(user_id)
    send_friend_update(friend_id)
    send_new_friend_notification(friend_id, user_id)
    return JsonResponse(
        {"status": "success", "message": f"{friend.username} added as a friend."}
    )


@csrf_exempt
@require_http_methods(["DELETE"])
def remove_friend(request, user_id, friend_id):
    user = get_object_or_404(User, pk=user_id)
    friend = get_object_or_404(User, pk=friend_id)
    Friend.objects.filter(user=user, friend=friend).delete()
    send_friend_update(user_id)
    send_friend_update(friend_id)
    return JsonResponse(
        {"status": "success", "message": f"{friend.username} removed from friends."}
    )


# Recovery of login and user name by token, for test purposes only at the moment.
@require_http_methods(["GET"])
def authenticate_user(request, token):
    user = get_object_or_404(User, token=token)
    return JsonResponse({"user_id": user.user_id, "username": user.username})


@require_http_methods(["GET"])
def list_friends(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    friends = user.user_friends.all()
    friend_list = [
        {"user_id": friend.friend.user_id, "username": friend.friend.username}
        for friend in friends
    ]
    return JsonResponse({"friends": friend_list})

# /api/user/friends/follows/<int:user_id>/<int:friend_id>/
# Returns whether user_id follows friend_id
@require_http_methods(["GET"])
def is_following(request, user_id, friend_id):
    return JsonResponse({"is_following": Friend.objects.filter(user_id=user_id, friend_id=friend_id).exists()})

# https://channels.readthedocs.io/en/stable/topics/channel_layers.html#groups
# type: name of the method that will receive the message
def send_friend_update(user_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}", {"type": "friend_list_update", "user_id": user_id}
    )

def send_new_friend_notification(target_id, user_id):
    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)(
        f"user_{target_id}", {"type": "new_follower", "follower_username": User.objects.get(user_id=user_id).username}
    )
