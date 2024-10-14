import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
import ft_requests
import traceback
from threading import Thread
import logging
from ..user import user_status

USERS_SERVICE_URL = "http://users-service:8001/api"
PONG_SERVICE_URL = "http://pong-service:8002/api"

# https://channels.readthedocs.io/en/latest/topics/consumers.html#websocketconsumer
# https://channels.readthedocs.io/en/stable/topics/channel_layers.html#groups
class PongGameConsumer(AsyncWebsocketConsumer):
    group_user_count = {}

    # Called on connection
    async def connect(self):
        self.user_token = self.scope['url_route']['kwargs']['token']
        self.game_id = self.scope['url_route']['kwargs']['game_id']

        self.user_id = await self.authenticate_user(self.user_token)
        if self.user_id:
            await self.accept()
            logging.getLogger("websocket_logger").info('Accepted new pong game connection from user %d.', self.user_id)
            await self.channel_layer.group_add(
                f"pong_game_{self.game_id}",
                self.channel_name
            )
            # debug message
            await self.channel_layer.group_send(
                    f"pong_game_{self.game_id}",
                    {
                        "type": "user_connected",
                        "game_id": self.game_id,
                        "user_id": self.user_id,
                    }
                )
            await self.update_group_size(self.game_id, increment=True)
            # debug log
            logging.getLogger("websocket_logger").info(f"Game {self.game_id} websocket size is now {await self.get_group_size(self.game_id)}")

            if await self.get_group_size(self.game_id) == 2:
                await self.start_game()
        else:
            await self.close()

    # Called with either text_data or bytes_data for each frame
    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            logging.getLogger("websocket_logger").info('Received pong game data from user %d:\n%s', self.game_id, data)
        except:
            logging.getLogger("websocket_logger").info('Invalid pong game data from user %d:\n%s', self.game_id, data)

    # Called when the socket closes
    async def disconnect(self, close_code):
        if self.game_id:
            logging.getLogger("websocket_logger").info('Pong game User %d disconnected.', self.user_id)
            await self.channel_layer.group_discard(
                f"pong_game_{self.game_id}",
                self.channel_name
            )
            await self.update_group_size(self.game_id, increment=False)


    async def authenticate_user(self, token):
        logging.getLogger("websocket_logger").info('Attempting to authenticate pong game user with token "%s"...', token)
        try:
            user_resp = ft_requests.get(f'{USERS_SERVICE_URL}/user/authenticate/{token}/')
            user_resp.raise_for_status()
            user_data = user_resp.json()
            logging.getLogger("websocket_logger").info('Found pong game user with id %d.', user_data['user_id'])
            return user_data['user_id']
        except ft_requests.exceptions.RequestException:
            return None
        
    @database_sync_to_async
    def update_group_size(self, game_id, increment):
        if game_id not in self.group_user_count:
            self.group_user_count[game_id] = 0
        
        if increment:
            self.group_user_count[game_id] += 1
        else:
            self.group_user_count[game_id] -= 1

    async def get_group_size(self, game_id):
        return self.group_user_count.get(game_id, 0)

    
    async def user_connected(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_connected',
            'game_id': event['game_id'],
            'user_id': event['user_id'],
        }))
    

    async def start_game(self):
        try:
            data = {
                'game_id': self.game_id
            }
            game_resp = ft_requests.post(f'{PONG_SERVICE_URL}/game/start/', data=data)
            game_resp.raise_for_status()
            game_resp = game_resp.json()
            logging.getLogger("websocket_logger").info(f"Game {self.game_id} sent start message")
        except:
            logging.getLogger("websocket_logger").info(f"Failed to start game {self.game_id}")


    async def game_state_update(self, event):
        state = event['state']
        logging.getLogger("websocket_logger").info('Received game state update for game %d', state['game_id'])
        await self.send(text_data=json.dumps({"type": "game_state_update", "state": state}))