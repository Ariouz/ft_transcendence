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

    logging.getLogger("django").info(f"Creating game with {players}")

    if type == "local1v1":
        players.pop() # removed duplicated user (double websocket issue)

    for user_id in players:
        async_to_sync(channel_layer.group_send)(
            f"pong_user_{user_id}", {
                "type": "game_create",
                "game_id": game.game_id
            }
        )

        # async_to_sync(channel_layer.group_add)(
        #     f"pong_game_{game.game_id}",
        #     f"pong_user_{user_id}"
        # )


@sync_to_async
def get_game(game_id):
    return PongGame.objects.get(game_id=game_id)


async def start_game(game_id):
    game = await get_game(game_id)
    if (game.status != "init"):
        return
    await set_game_status(game.game_id, "started")

    players_ids = [int(player) for player in game.users]

    game_state = PongGameState(game_id=game.game_id,  player1_id=players_ids[0], player2_id=players_ids[1], type=game.type)
    logging.getLogger("django").info(f"Starting {game.type} game {game.game_id}")
    
    await game_loop(game_state=game_state, players=players_ids)


async def game_loop(game_state:PongGameState, players):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        redis_task = asyncio.run(listen_to_redis(game_state))
    else:
        redis_task = loop.create_task(listen_to_redis(game_state))

    await time_ball(players, game_state, "")

    while await game_state.is_running():
        await asyncio.sleep(0.016)

        if await game_state.is_paused():
            continue

        # if await game_state.get_has_disconnected():
        #     game_state.reset_ball()
        #     continue

        game_state.update_ball_pos()

        game_state.check_ball_wall_collision()
        game_state.check_ball_paddle_collision()

        scoring_player = game_state.check_score()
        if not scoring_player == "":
            await time_ball(players, game_state, scoring_player)

        game_data = await game_state.get_state()
        await pong_game_ws_update.send_game_state_to_players(game_data)
        # logging.getLogger("django").info(f"Game loop {game_state.game_id}")

        if game_state.check_win():
            await pong_game_ws_update.send_winner_to_players(game_state.get_winner(), await game_state.get_state(), 5)
            await game_state.set_paused(True)
            await game_state.set_running(False)
            await pong_game_ws_update.send_game_state_to_players(await game_state.get_state())
            if not redis_task.done():
                redis_task.cancel()
                try:
                    await redis_task
                except asyncio.CancelledError:
                    pass
            await save_game_to_db(game_state)

@sync_to_async
def set_game_status(game_id, game_status):
    game = PongGame.objects.get(game_id=game_id)
    game.status = game_status
    game.save()


@sync_to_async
def save_game_to_db(game_state:PongGameState):
    game = PongGame.objects.get(game_id=game_state.game_id)
    
    game.score = [game_state.players['player1']['score'], game_state.players['player2']['score']]
    game.winner_id = game_state.get_player_id(game_state.get_winner())
    game.status = "finished"
    game.save()

    # todo save users' stats and history


async def time_ball(players, game_state:PongGameState, scoring_player, sendStartTimer=True, is_reconnect=False):
    was_paused = False
    if await game_state.is_paused():
        was_paused = True

    await game_state.set_paused(True)
    game_state.reset_ball()
    game_state.reset_players_pos()
    game_state.ball_velocity = {'x': 0, 'y': 0}

    ball_timer = 5 # seconds before restart
    if not scoring_player == "" and not was_paused:
        await pong_game_ws_update.send_scored_to_players(scoring_player, await game_state.get_state(), ball_timer)
    elif sendStartTimer and not was_paused:
        await pong_game_ws_update.send_start_timer(await game_state.get_state(), ball_timer)

    await pong_game_ws_update.send_game_state_to_players(await game_state.get_state())
    await asyncio.sleep(ball_timer)


    if await game_state.get_has_disconnected() and not is_reconnect:
        logging.getLogger("django").info(f"Player has disconnected during the timer, game paused")
        await game_state.set_paused(True)
        await pong_game_ws_update.send_game_state_to_players(await game_state.get_state())
        return

    await game_state.set_paused(False)
    game_state.reset_ball()




async def listen_to_redis(game_state:PongGameState):
    redis_client = await redis.asyncio.Redis.from_url('redis://redis-websocket-users:6379')
    logging.getLogger("django").info(f"Ready to listen redis on pong_game_{game_state.game_id}_stream")
    last_id = '0'

    try:
        while await game_state.is_running():
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
    except asyncio.CancelledError as e:
        logging.getLogger("django").info(f"Redis listener task cancelled for game {game_state.game_id}: {str(e)}")
        raise
    except Exception as e:
        logging.getLogger("django").error(f"Error in Redis listener for game {game_state.game_id}: {str(e)}")
    finally:
        await redis_client.close()


async def handle_redis_message(message_data, game_state:PongGameState):
    if not message_data['type']:
        return

    if message_data['type'] == "player_move":
        if await game_state.is_paused() or not await game_state.is_running():
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

    elif message_data['type'] == "pong_game_user_disconnected":
        if not await game_state.is_running():
            return
        
        if not message_data['user_id']:
            return
        user_id = message_data['user_id']

        await game_state.set_has_disconnected(True)
        if not game_state.game_pause_task:
            game_state.game_pause_task = asyncio.create_task(pause_game_user_disconnected(game_state, user_id))
        # logging.getLogger("django").info(f"User {user_id} disconnected on game {game_state.game_id}")
    elif message_data['type'] == "pong_game_user_connected":
        if not await game_state.is_running():
            return
        
        if not message_data['user_id']:
            return
        user_id = message_data['user_id']

        game_state.connected_users.add(user_id)
        if game_state.game_pause_task:
            if  not game_state.game_pause_task.cancelled():
                game_state.game_pause_task.cancel()
                game_state.game_pause_task = None
                logging.getLogger("django").info(f"Cancelling disconnect task on game {game_state.game_id}")
            
            logging.getLogger("django").info(f"User {user_id} reconnected on game {game_state.game_id}")
            await pong_game_ws_update.send_reconnected_to_players(await game_state.get_player_by_id(user_id), await game_state.get_state(), 5)
            await game_state.set_paused(False)
            await time_ball([], game_state, "", sendStartTimer=False, is_reconnect=True)
            await game_state.set_has_disconnected(False)


async def pause_game_user_disconnected(game_state:PongGameState, user_id):
    # allow 30s to reconnect
    allowed_time = 10
    try:
        logging.getLogger("django").info(f"User {user_id} disconnected on game {game_state.game_id}")

        await game_state.set_paused(True)
        logging.getLogger("django").info(f"Game {game_state.game_id} is now paused.")
        game_state.connected_users.remove(user_id)

        player = await game_state.get_player_by_id(user_id)
        await pong_game_ws_update.send_game_state_to_players(await game_state.get_state())
        logging.getLogger("django").info(f"Sent pause game state to {game_state.game_id}")
        await pong_game_ws_update.send_disconnect_pause_to_players(player, await game_state.get_state(), allowed_time)
        logging.getLogger("django").info(f"Starting {allowed_time}s pause timer on game {game_state.game_id}")
        await asyncio.sleep(allowed_time)
        logging.getLogger("django").info(f"Ended timer on game {game_state.game_id}")

        logging.getLogger("django").info(f"Users in game {game_state.connected_users}")
        if not user_id in game_state.connected_users:
            logging.getLogger("django").info(f"User {user_id} didn't reconnect on game {game_state.game_id}")
            opponent = "player1" if game_state.get_player_by_id(user_id) == "player2" else "player2"
            game_state.players[opponent]['score'] = 5
            await game_state.set_paused(False)

    except Exception as e:
        logging.getLogger("django").info(f"User {user_id} reconnection task cancelled on game {game_state.game_id} {str(e)}")
        game_state.game_pause_task = None

