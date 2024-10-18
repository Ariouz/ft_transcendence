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
from . import pong_game_ws_update

def create_game(players, type):
    game = PongGame.objects.create(users=players, type=type)
    game.save()
    channel_layer = get_channel_layer()

    logging.getLogger("django").info(f"Creating game for with {players}")

    if type == "local1v1":
        players.pop() # removed duplicated user (double websocket issue)

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

    game_state = PongGameState(game_id=game.game_id,  player1_id=players_ids[0], player2_id=players_ids[1], type=game.type)
    logging.getLogger("django").info(f"Starting {game.type} game {game.game_id}")
    
    await game_loop(game_state=game_state, players=players_ids)



async def game_loop(game_state:PongGameState, players):
    redis_task = asyncio.create_task(listen_to_redis(game_state))

    await time_ball(players, game_state, "")

    while game_state.is_running:
        await asyncio.sleep(0.016)

        game_state.update_ball_pos()

        game_state.check_ball_wall_collision()
        game_state.check_ball_paddle_collision()

        scoring_player = game_state.check_score()
        if not scoring_player == "":
            await time_ball(players, game_state, scoring_player)

        game_data = game_state.get_state()
        await pong_game_ws_update.send_game_state_to_players(players, game_data)
        # logging.getLogger("django").info(f"Game loop {game_state.game_id}")

        if game_state.check_win():
            await pong_game_ws_update.send_winner_to_players(game_state.get_winner(), game_state.get_state(), 5)
            game_state.is_paused = True
            game_state.is_running = False
            await pong_game_ws_update.send_game_state_to_players(players, game_state.get_state())
            redis_task.cancel()
            await save_game_to_db(game_state)
            try:
                await redis_task
            except:
                pass

@sync_to_async
def save_game_to_db(game_state:PongGameState):
    game = PongGame.objects.get(game_id=game_state.game_id)
    
    game.score = [game_state.players['player1']['score'], game_state.players['player2']['score']]
    game.winner_id = game_state.get_player_id(game_state.get_winner())
    game.status = "finished"
    game.save()

    # todo save users' stats and history


async def time_ball(players, game_state:PongGameState, scoring_player):
    game_state.is_paused = True
    game_state.reset_ball()
    game_state.reset_players_pos()
    game_state.ball_velocity = {'x': 0, 'y': 0}

    ball_timer = 5 # seconds before restart
    if not scoring_player == "":
        await pong_game_ws_update.send_scored_to_players(scoring_player, game_state.get_state(), ball_timer)
    else:
        await pong_game_ws_update.send_start_timer(game_state.get_state(), ball_timer)

    await pong_game_ws_update.send_game_state_to_players(players, game_state.get_state())
    await asyncio.sleep(ball_timer)
    game_state.is_paused = False
    game_state.reset_ball()




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

    if message_data['type'] == "player_move":
        if game_state.is_paused or not game_state.is_running:
            return

        if not message_data['data'] or not isinstance(message_data['data'], list):
            return
        
        for data in message_data['data']:
            if not data['player_paddle']:
                continue
            player_paddle = data['player_paddle']
            if not data['direction']:
                continue
            direction = data['direction']
            
            game_state.move_player(player_paddle, direction)

