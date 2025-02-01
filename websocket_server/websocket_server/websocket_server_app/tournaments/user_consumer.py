import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import ft_requests
import traceback
from threading import Thread
import logging
from ..user import user_status
import redis

USERS_SERVICE_URL = "https://users-service:8001/api"
PONG_SERVICE_URL = "https://pong-service:8002/api"

# https://channels.readthedocs.io/en/latest/topics/consumers.html#websocketconsumer
# https://channels.readthedocs.io/en/stable/topics/channel_layers.html#groups

class TournamentUserConsumer(WebsocketConsumer):
    # Called on connection
    def connect(self):
        self.user_token = self.scope['url_route']['kwargs']['token']

        self.user_id = self.authenticate_user(self.user_token)
        if self.user_id:
            self.accept()
            logging.getLogger("websocket_logger").info('Accepted new pong connection from user %d.', self.user_id)
            async_to_sync(self.channel_layer.group_add)(
                f"tournament_user_{self.user_id}",
                self.channel_name
            )
        else:
            self.close()

    # Called with either text_data or bytes_data for each frame
    def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            logging.getLogger("websocket_logger").info('Received tournament data from user %d:\n%s', self.user_id, data)
        except:
            logging.getLogger("websocket_logger").info('Invalid tournament data from user %d:\n%s', self.user_id, data)

    # Called when the socket closes
    def disconnect(self, close_code):
        if self.user_id:
            logging.getLogger("websocket_logger").info('Tournament User %d disconnected.', self.user_id)
            async_to_sync(self.channel_layer.group_discard)(
                f"tournament_user_{self.user_id}",
                self.channel_name
            )

    def authenticate_user(self, token):
        logging.getLogger("websocket_logger").info('Attempting to authenticate tournament user with token "%s"...', token)
        try:
            user_resp = ft_requests.get(f'{USERS_SERVICE_URL}/user/authenticate/{token}/')
            if not user_resp.status == 200:
                return None
            user_data = user_resp.json()
            logging.getLogger("websocket_logger").info('Found tournament user with id %d.', user_data['user_id'])
            return user_data['user_id']
        except ft_requests.exceptions.RequestException:
            return None
    

    def joined_tournament(self, event):
        tournament_id = event['tournament_id']
        logging.getLogger("websocket_logger").info('Tournament joined message with id %d.', tournament_id)
        self.send(text_data=json.dumps({"type":"joined_tournament", "tournament_id": tournament_id}))