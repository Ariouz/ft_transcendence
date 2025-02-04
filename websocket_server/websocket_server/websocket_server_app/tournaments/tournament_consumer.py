import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
import ft_requests
from threading import Thread
import logging
from ..user import user_status

USERS_SERVICE_URL = "https://users-service:8001/api"
PONG_SERVICE_URL = "https://pong-service:8002/api"

# https://channels.readthedocs.io/en/latest/topics/consumers.html#websocketconsumer
# https://channels.readthedocs.io/en/stable/topics/channel_layers.html#groups
class TournamentConsumer(AsyncWebsocketConsumer):
    group_user_count = {}

    # Called on connection
    async def connect(self):
        self.user_token = self.scope['url_route']['kwargs']['token']
        self.tournament_id = self.scope['url_route']['kwargs']['tournament_id']

        self.user_id = await self.authenticate_user(self.user_token)
        if self.user_id:
            await self.accept()
            logging.getLogger("websocket_logger").info('Accepted new tournament connection from user %d.', self.user_id)
            await self.channel_layer.group_add(
                f"tournament_{self.tournament_id}",
                self.channel_name
            )
            # debug message
            await self.channel_layer.group_send(
                    f"tournament_{self.tournament_id}",
                    {
                        "type": "user_joined",
                        "tournament_id": self.tournament_id,
                        "user_id": self.user_id,
                    }
                )
            await self.update_group_size(self.tournament_id, increment=True)

        else:
            await self.close()

    # Called with either text_data or bytes_data for each frame
    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
        except:
            logging.getLogger("websocket_logger").info('Invalid pong game data from game %d:\n%s', self.tournament_id, data)

    # Called when the socket closes
    async def disconnect(self, close_code=0):
        if self.tournament_id:

            await self.channel_layer.group_send(
                    f"tournament_{self.tournament_id}",
                    {
                        "type": "user_left",
                        "tournament_id": self.tournament_id,
                        "user_id": self.user_id,
                    }
                )
            
            logging.getLogger("websocket_logger").info('Tournament participant %d disconnected.', self.user_id)
            await self.channel_layer.group_discard(
                f"tournament_{self.tournament_id}",
                self.channel_name
            )
            await self.update_group_size(self.tournament_id, increment=False)
            logging.getLogger("websocket_logger").info(f"Game {self.tournament_id} websocket size is now {await self.get_group_size(self.tournament_id)}")


    async def authenticate_user(self, token):
        logging.getLogger("websocket_logger").info('Attempting to authenticate tournament participant with token "%s"...', token)
        try:
            user_resp = ft_requests.get(f'{USERS_SERVICE_URL}/user/authenticate/{token}/')
            if not user_resp.status == 200:
                return None
            user_data = user_resp.json()
            logging.getLogger("websocket_logger").info('Found tournament participant with id %d.', user_data['user_id'])
            return user_data['user_id']
        except ft_requests.exceptions.RequestException:
            return None
        
    @database_sync_to_async
    def update_group_size(self, tournament_id, increment):
        if tournament_id not in self.group_user_count:
            self.group_user_count[tournament_id] = 0
        
        if increment:
            self.group_user_count[tournament_id] += 1
        else:
            self.group_user_count[tournament_id] -= 1

    async def get_group_size(self, tournament_id):
        return self.group_user_count.get(tournament_id, 0)

    
    async def user_joined(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_joined',
            'tournament_id': event['tournament_id'],
            'user_id': event['user_id'],
        }))

    async def user_left(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_left',
            'tournament_id': event['tournament_id'],
            'user_id': event['user_id'],
        }))

    async def ws_disconnect_user(self, event):
        user_id = event['user_id']
        if self.user_id == user_id:
            self.disconnect()