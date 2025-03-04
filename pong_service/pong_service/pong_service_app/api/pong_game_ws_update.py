from channels.layers import get_channel_layer
from pong_service_app.models import *

async def send_game_state_to_players(game_data):
    channel_layer = get_channel_layer()

    await channel_layer.group_send(
        f"pong_game_{game_data['game_id']}",
        {
            "type": "game_state_update",
            "state": game_data
        })

async def send_scored_to_players(scoring_player, game_data, ball_timer):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"pong_game_{game_data['game_id']}",
        {
            "type": "game_player_scored",
            "state": game_data,
            "scoring_player": scoring_player,
            "countdown_timer": ball_timer
        })

async def send_start_timer(game_data, ball_timer):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"pong_game_{game_data['game_id']}",
        {
            "type": "game_start_timer",
            "countdown_timer": ball_timer
        })
    
async def send_winner_to_players(winner, game_data, ball_timer, tournament_id):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"pong_game_{game_data['game_id']}",
        {
            "type": "game_winner_timer",
            "state": game_data,
            "winner": winner,
            "countdown_timer": ball_timer,
            "tournament_id": tournament_id if tournament_id else -1
        })
    
    
async def send_disconnect_pause_to_players(player, game_data, end_timer):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"pong_game_{game_data['game_id']}",
        {
            "type": "game_user_disconnected",
            "state": game_data,
            "player": player,
            "countdown_timer": end_timer
        })
    
    
async def send_reconnected_to_players(player, game_data, end_timer):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"pong_game_{game_data['game_id']}",
        {
            "type": "game_user_reconnected",
            "state": game_data,
            "player": player,
            "countdown_timer": end_timer
        })

