from .objects.pong_game_state import PongGameState
from channels.layers import get_channel_layer
import random

import logging


#### EVENTS ######
async def send_game_event_spawn(game_id, event_type):
    logging.getLogger("django").info(f"Sending {event_type}")
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"pong_game_{game_id}",
        {
            "type": "game_event_spawn",
            "event_type": event_type
        })
    logging.getLogger("django").info(f"Sent {event_type}")
    

events = {"malus_ball_flicker":0.7, "theme":0.3}
async def tick_game_event_spawn(game_state:PongGameState):
    rand = random.random()
    if rand >= 0.5 and rand <= 0.501:
        keys = list(events.keys())
        vals = list(events.values())
        event = random.choices(keys, vals, k=1)
        await send_game_event_spawn(game_state.game_id, event[0])


