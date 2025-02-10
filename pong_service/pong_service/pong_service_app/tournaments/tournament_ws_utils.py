from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from pong_service_app.models import *

TOURNAMENT_USER = "tournament_user_"
TOURNAMENT = "tournament_"

# user ws
def join_user(user_id, tournament_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"{TOURNAMENT_USER}{user_id}", {
            "type": "joined_tournament",
            "tournament_id": tournament_id
        }
    )

# user ws
def ws_connect_user(user_id, tournament_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"{TOURNAMENT_USER}{user_id}", {
            "type": "ws_connect_user",
            "tournament_id": tournament_id
        }
    )

# group ws
def ws_disconnect_user(user_id, tournament_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"{TOURNAMENT}{tournament_id}", {
            "type": "ws_disconnect_user",
            "user_id": user_id
        }
    )

# tournament ws
def send_tournament_delete(tournament_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"{TOURNAMENT}{tournament_id}", {
            "type": "tournament_delete",
        }
    )


# tournament ws
def send_round_update(match: TournamentMatch):
    data = {}
    data['match_id'] = match.pk
    data['round'] = match.round
    data['score1'] = match.score1
    data['score2'] = match.score2
    data['winner'] = match.winner.user_id if match.winner else -1

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"{TOURNAMENT}{match.tournament.tournament_id}", {
            "type": "tournament_round_update",
            "data": data
        }
    )

# tournament ws
def send_rounds_generated(tournament_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"{TOURNAMENT}{tournament_id}", {
            "type": "rounds_generated",
            "tournament_id": tournament_id
        }
    )

# tournament ws
def send_tournament_started(tournament_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"{TOURNAMENT}{tournament_id}", {
            "type": "tournament_started",
            "tournament_id": tournament_id
        }
    )


# tournament ws
def send_tournament_ended(tournament_id, winner_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"{TOURNAMENT}{tournament_id}", {
            "type": "tournament_ended",
            "tournament_id": tournament_id,
            "winner_id": winner_id
        }
    )