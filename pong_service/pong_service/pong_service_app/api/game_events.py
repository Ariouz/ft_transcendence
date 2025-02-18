from .objects.pong_game_state import PongGameState
from channels.layers import get_channel_layer
from . import themes

import asyncio
import random

import logging


#### EVENTS ######
async def send_game_event_spawn(game_id, event_type, event_data):
    logging.getLogger("django").info(f"Sending {event_type}")
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"pong_game_{game_id}",
        {
            "type": "game_event_spawn",
            "event_type": event_type,
            "event_data": event_data
        })
    logging.getLogger("django").info(f"Sent {event_type}")
    

events = {
    "malus_ball_flicker": 0.25,
    "ball_speed": 0.75
}

events_data = {
    "malus_ball_flicker": 5,
    "ball_speed": 0.4
}

async def tick_game_event_spawn(game_state:PongGameState):
    if game_state.game_type != "arcade": return
    try:
        while await game_state.is_running():
            await asyncio.sleep(8)
            if await game_state.is_paused(): continue
            
            rand = random.randint(1, 10)
            if rand >= 8:
                keys = list(events.keys())
                vals = list(events.values())
                event = random.choices(keys, vals, k=1)[0]

                data  = events_data[event]
                if event == "ball_speed":
                    data = round(random.uniform(-data*data, data), 2) or 0.05
                    game_state.ball_velocity['x'] *= 1 + data
                    game_state.ball_velocity['y'] *= 1 + data

                await send_game_event_spawn(game_state.game_id, event, data)

    except asyncio.CancelledError as e:
        logging.getLogger("django").info(f"Events task cancelled for game {game_state.game_id}: {str(e)}")
        raise
    


