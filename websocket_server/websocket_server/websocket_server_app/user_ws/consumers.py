import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import ft_requests
import traceback
from threading import Thread
import logging
from ..user import user_status

USERS_SERVICE_URL = "https://users-service:8001/api"

# https://channels.readthedocs.io/en/latest/topics/consumers.html#websocketconsumer
# https://channels.readthedocs.io/en/stable/topics/channel_layers.html#groups
class FriendsConsumer(WebsocketConsumer):
    # Called on connection
    def connect(self):
        self.user_token = self.scope['url_route']['kwargs']['token']
        self.user_id = self.authenticate_user(self.user_token)
        if self.user_id:
            self.accept()
            logging.getLogger("websocket_logger").info('Accepted new connection from user %d.', self.user_id)
            Thread(target=self.fetch_friends).start()
            async_to_sync(self.channel_layer.group_add)(
                f"user_{self.user_id}",
                self.channel_name
            )
            user_status.set_user_online(self.user_id)
        else:
            logging.getLogger("websocket_logger").info('Rejected connection')
            self.close()

    # Called with either text_data or bytes_data for each frame
    def receive(self, text_data=None, bytes_data=None):

        data = json.loads(text_data)
        logging.getLogger("websocket_logger").info('Received data from user %d:\n%s', self.user_id, data)

    # Called when the socket closes
    def disconnect(self, close_code):
        if self.user_id:
            logging.getLogger("websocket_logger").info('User %d disconnected.', self.user_id)
            async_to_sync(self.channel_layer.group_discard)(
                f"user_{self.user_id}",
                self.channel_name
            )
            user_status.set_user_offline(self.user_id)

    def authenticate_user(self, token):
        logging.getLogger("websocket_logger").info('Attempting to authenticate user with token "%s"...', token)
        try:
            user_resp = ft_requests.get(f'{USERS_SERVICE_URL}/user/authenticate/{token}/')
            if not user_resp.status == 200:
                return None
            user_data = user_resp.json()
            logging.getLogger("websocket_logger").info('Found user with id %d.', user_data['user_id'])
            return user_data['user_id']
        except Exception as e:
            logging.getLogger("websocket_logger").info(f'Error while authenticating: {e}')
            return None

    def fetch_friends(self):
        logging.getLogger("websocket_logger").info('Fetching user %d\'s friends...', self.user_id)
        try:
            friends_resp = ft_requests.get(f'{USERS_SERVICE_URL}/user/friends/{self.user_id}/')
            friends_resp.raise_for_status()
            friends_data = friends_resp.json()
            self.send(text_data=json.dumps(friends_data))
        except ft_requests.exceptions.RequestException as e:
            error_message = {
                'error': 'Failed to fetch friends',
                'details': str(e),
                'traceback': traceback.format_exc()
            }
            self.send(text_data=json.dumps(error_message))

    # Method called by the reception of a message sent, on the channel,
    # by the send_friend_update function in users_service
    def friend_list_update(self, event):
        logging.getLogger("websocket_logger").info('Updating user %d\'s friend list...', self.user_id)
        user_id = event['user_id']
        self.update_friend_list(user_id)

    def update_friend_list(self, user_id):
        try:
            friends_resp = ft_requests.get(f'{USERS_SERVICE_URL}/user/friends/{user_id}/')
            friends_resp.raise_for_status()
            friends_data = friends_resp.json()
            self.send(text_data=json.dumps(friends_data))
        except ft_requests.exceptions.RequestException as e:
            error_message = {
                'error': 'Failed to update friends list',
                'details': str(e),
                'traceback': traceback.format_exc()
            }
            self.send(text_data=json.dumps(error_message))

    def new_follower(self, event):
        follower_username = event['follower_username']
        self.send(text_data=json.dumps({"type":"new_follower_notification", "follower_username": follower_username}))

        
