from users_service_app.models import User, Friend
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from users_service_app.response_messages import error_response, json_response, get_translation


@require_http_methods(["GET"])
def list_friends(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    friends = Friend.objects.filter(user=user).select_related("friend")
    friend_list = [
        {"user_id": friend.friend.user_id, "username": friend.friend.username}
        for friend in friends
    ]
    return json_response({"friends": friend_list})


@require_http_methods(["POST"])
def add_friend(request, user_id, friend_id):
    user = get_object_or_404(User, pk=user_id)
    friend = get_object_or_404(User, pk=friend_id)
    if Friend.objects.filter(user=user, friend=friend).exists():
        return json_response({"status": "error", "message": get_translation(request, "already_a_friend", friend.username)})
    Friend.objects.create(user=user, friend=friend)
    send_friend_update(user_id)
    send_friend_update(friend_id)
    send_new_friend_notification(friend_id, user_id)
    return json_response({"status": "success", "message": get_translation(request, "added_as_a_friend", friend.username)})


@require_http_methods(["DELETE"])
def remove_friend(request, user_id, friend_id):
    user = get_object_or_404(User, pk=user_id)
    friend = get_object_or_404(User, pk=friend_id)
    if not Friend.objects.filter(user=user, friend=friend).exists():
        return json_response({"status": "error", "message": get_translation(request, "not_a_friend", friend.username)})
    Friend.objects.filter(user=user, friend=friend).delete()
    send_friend_update(user_id)
    send_friend_update(friend_id)
    return json_response(
        {"status": "success", "message": get_translation(request, "removed_from_friends", friend.username)}
    )


@require_http_methods(["GET"])
def authenticate_user(request, token):
    if not User.objects.filter(token=token).exists():
        return error_response(request, "user_not_found", "cannot_find_user_with_this_token", status_code=404)
    user = User.objects.filter(token=token).get()
    return json_response({"user_id": user.user_id, "username": user.username})

# /api/user/friends/follows/<int:user_id>/<int:friend_id>/
# Returns whether user_id follows friend_id
@require_http_methods(["GET"])
def is_following(request, user_id, friend_id):
    return json_response({"is_following": Friend.objects.filter(user_id=user_id, friend_id=friend_id).exists()})

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
