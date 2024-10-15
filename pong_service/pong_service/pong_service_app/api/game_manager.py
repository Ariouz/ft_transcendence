from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from pong_service_app.models import *
from .objects.pong_game_state import PongGameState
import ft_requests
import json
import logging
import asyncio
import redis.asyncio


def create_game(players):
    game = PongGame.objects.create(users=players)
    game.save()
    channel_layer = get_channel_layer()

    logging.getLogger("django").info(f"Creating game for with {players}")

    for user_id in players:
        async_to_sync(channel_layer.group_send)(
            f"pong_user_{user_id}", {
                "type": "game_create",
                "game_id": game.game_id
            }
        )

        async_to_sync(channel_layer.group_add)(
            f"pong_game_{game.game_id}",
            f"pong_user_{user_id}"
        )


@sync_to_async
def get_game(game_id):
    return PongGame.objects.get(game_id=game_id)


async def start_game(game_id):
    game = await get_game(game_id)

    players_ids = [int(player) for player in game.users]

    game_state = PongGameState(game_id=game.game_id,  player1_id=players_ids[0], player2_id=players_ids[1])
    logging.getLogger("django").info(f"Starting game {game.game_id}")
    
    await game_loop(game_state=game_state, players=players_ids)



async def game_loop(game_state:PongGameState, players):
    redis_task = asyncio.create_task(listen_to_redis(game_state))

    while game_state.is_running:
        await asyncio.sleep(0.016)

        game_state.update_ball_pos() # ce code fait juste +1 sur la position

        # todo check collisions

        game_data = game_state.get_state()
        await send_game_state_to_players(players, game_data)
        # logging.getLogger("django").info(f"Game loop {game_state.game_id}")

        if game_state.ball_position['y'] >= 400:
            game_state.is_running = False
            redis_task.cancel()
            try:
                await redis_task
            except:
                pass



async def send_game_state_to_players(players, game_data):
    channel_layer = get_channel_layer()

    # logging.getLogger("django").info(f"Game update sending to {game_data["game_id"]} with data {game_data}")

    await channel_layer.group_send(
        f"pong_game_{game_data['game_id']}",
        {
            "type": "game_state_update",
            "state": game_data
        }
    )

    # logging.getLogger("django").info(f"Game update sent to {game_data["game_id"]}")


async def listen_to_redis(game_state:PongGameState):
    redis_client = await redis.asyncio.Redis.from_url('redis://redis-websocket-users:6379')
    logging.getLogger("django").info(f"Ready to listen redis on pong_game_{game_state.game_id}_stream")
    last_id = '0'

    try:
        while game_state.is_running:
            stream_data = await redis_client.xread({f"pong_game_{game_state.game_id}_stream": last_id}, count=1, block=1000)
            if stream_data:
                for stream in stream_data:
                    last_id = stream[1][0][0]

                    stream_name, messages = stream
                    for msg_id, message_data in messages:
                        message_str = message_data[b'message'].decode("utf-8")
                        message_dict = json.loads(message_str)
                        logging.getLogger("django").info(f"received msg from redis {message_dict}")
                        await handle_redis_message(message_dict, game_state)

            await asyncio.sleep(0.016)
    except asyncio.CancelledError:
        raise
    except:
        pass
    finally:
        await redis_client.close()


async def handle_redis_message(message_data, game_state:PongGameState):
    if not message_data['type']:
        return
    # {'type': 'player_move', 'data': {'player_paddle': 'player1', 'direction': 'DOWN'}}

    if message_data['type'] == "player_move":
        if not message_data['data']:
            return
        data = message_data['data']
        if not data['player_paddle']:
            return
        player_paddle = data['player_paddle']
        if not data['direction']:
            return
        direction = data['direction']
        game_state.move_player(player_paddle, direction)
        logging.getLogger("django").info(f"Moved {player_paddle} {direction}")


