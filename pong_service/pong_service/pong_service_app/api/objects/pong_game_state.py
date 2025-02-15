import random
import asyncio

class PongGameState:
    def __init__(self, game_id, player1_id, player2_id, type):
        self.game_id = game_id
        self.game_type = type

        self.canvas = {
            'width': 800,
            'height': 400
        }

        self.paddle = {
            'width': 10,
            'height': 70,
            'speed': 7
        }

        self.players = {
            'player1': {
                'id': player1_id,
                'position': {
                    'x': 0, 
                    'y': (self.canvas['height'] - self.paddle['height']) // 2
                },
                'score': 0
            },
            'player2': {
                'id': player2_id,
                'position': {
                    'x': self.canvas['width'] - self.paddle['width'],
                    'y': (self.canvas['height'] - self.paddle['height']) // 2
                },
                'score': 0
            }
        }

        self.ball_position = {
            'x': self.canvas['width'] // 2,
            'y': self.canvas['height'] // 2
        }
        self.ball_velocity = {'x': 0, 'y': 0}
        self.ball_size = 10

        self.score_goal = 5

        self.running = True
        self.paused = False
        self.game_pause_task = None
        self.game_cancelled = False

        self.connected_users = set([player1_id, player2_id])
        self.has_disconnected = False

        self.first_disconnected = None

        self.lock = asyncio.Lock()
    
    def update_ball_pos(self):
        self.ball_position['x'] += self.ball_velocity['x']
        self.ball_position['y'] += self.ball_velocity['y']

    def check_ball_wall_collision(self):
        if self.ball_position['y'] <= 0 + self.ball_size:
            self.ball_velocity['y'] = abs(self.ball_velocity['y'])
        if self.ball_position['y'] >= self.canvas['height'] - self.ball_size:
            self.ball_velocity['y'] = -abs(self.ball_velocity['y'])

    def check_ball_paddle_collision(self):
        if self.ball_position['x'] <= self.paddle['width'] + self.ball_size:
            if self.players['player1']['position']['y'] - self.ball_size <= self.ball_position['y'] <= self.players['player1']['position']['y'] + self.paddle['height'] + self.ball_size:
                self.ball_velocity['x'] = abs(self.ball_velocity['x'])
                self.ball_velocity['x'] += 0.3
        
        if self.ball_position['x'] >= self.canvas['width'] - self.paddle['width'] - self.ball_size:
            if self.players['player2']['position']['y'] - self.ball_size <= self.ball_position['y'] <= self.players['player2']['position']['y'] + self.paddle['height'] + self.ball_size:
                self.ball_velocity['x'] = -abs(self.ball_velocity['x'])
                self.ball_velocity['x'] -= 0.3

    def check_score(self):
        if self.ball_position['x'] <= 0 + self.ball_size:
            self.players['player2']['score'] += 1
            self.reset_ball()
            if self.players['player2']['score'] >= self.score_goal:
                return ""
            return "player2"
        
        if self.ball_position['x'] >= self.canvas['width'] - self.ball_size:
            self.players['player1']['score'] += 1
            self.reset_ball()
            if self.players['player1']['score'] >= self.score_goal:
                return ""
            return "player1"
        return ""

    def random_ball_velocity(self):
        while True:
            velocity = random.uniform(-2.5, 2.5)
            if abs(velocity) > 1.5:
                return velocity

    def reset_ball(self):
        self.ball_position = {'x': self.canvas['width'] // 2, 'y': self.canvas['height'] // 2}
        self.ball_velocity = {'x': self.random_ball_velocity() * (1 + self.get_total_score() * 0.15), 'y': self.random_ball_velocity() / (1 + self.get_total_score() * 0.15)}


    def reset_players_pos(self):
        self.players['player1']['position']['x'] = 0, 
        self.players['player1']['position']['y'] = (self.canvas['height'] - self.paddle['height']) // 2

        self.players['player2']['position']['x'] = self.canvas['width'] - self.paddle['width']
        self.players['player2']['position']['y'] = (self.canvas['height'] - self.paddle['height']) // 2

    async def get_player_by_id(self, user_id):
        async with self.lock:
            if user_id == self.players['player1']['id']:
                return 'player1'
            elif user_id == self.players['player2']['id']:
                return 'player2'

    def move_player(self, player, direction):
        if direction == "UP":
            self.players[player]['position']['y'] = max(self.players[player]['position']['y'] - self.paddle['speed'], 0)
        elif direction == "DOWN":
            self.players[player]['position']['y'] = min(self.players[player]['position']['y'] + self.paddle['speed'], self.canvas['height'] - self.paddle['height'])
    
    def update_player_pos(self, user_id, position):
        if user_id == self.players['player1']['id']:
            self.players['player1']['position'] = position
        elif user_id == self.players['player2']['id']:
            self.players['player2']['position'] = position
    
    def get_total_score(self):
        return self.players['player1']['score'] + self.players['player2']['score']
    

    def check_win(self):
        return max(self.players['player1']['score'], self.players['player2']['score']) >= self.score_goal
    

    def get_winner(self):
        return "player1" if self.players['player1']['score'] >= self.score_goal else "player2"
    

    def get_player_id(self, player):
        return self.players[player]['id']
    

    async def is_paused(self):
        async with self.lock:
            return self.paused
        
    async def is_running(self):
        async with self.lock:
            return self.running
    
    async def set_paused(self, paused):
        async with self.lock:
            self.paused = paused
    
    async def set_running(self, running):
        async with self.lock:
            self.running = running

    async def set_pause_task(self, task):
        async with self.lock:
            self.game_pause_task = task

    async def get_has_disconnected(self):
        async with self.lock:
            return self.has_disconnected
        
    async def set_has_disconnected(self, val):
        async with self.lock:
            self.has_disconnected = val

    async def set_first_disconnected(self, val):
        async with self.lock:
            self.first_disconnected = val

    async def get_first_disconnected(self):
        async with self.lock:
            return self.first_disconnected

    async def get_state(self):
        async with self.lock:
            return {
                'game_id': self.game_id,
                'game_type': self.game_type,
                'canvas': self.canvas,
                'paddle': self.paddle,
                'players': self.players,
                'ball_position': self.ball_position,
                'running': self.running,
                'paused': self.paused,
            }