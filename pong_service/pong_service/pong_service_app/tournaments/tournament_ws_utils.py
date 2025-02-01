from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from pong_service_app.models import *

TOURNAMENT_USER = "tournament_user_"
TOURNAMENT = "tournament_"

# single ws
def connect_user(user_id, tournament_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"{TOURNAMENT_USER}{user_id}", {
            "type": "joined_tournament",
            "tournament_id": tournament_id
        }
    )

# single ws
def disconnect_user(user_id):
    pass

# group ws
def send_tournament_delete(tournament_id):
    pass

# group ws
def send_new_user(tournament_id):
    pass