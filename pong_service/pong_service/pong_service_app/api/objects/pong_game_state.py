class PongGameState:
    def __init__(self, game_id, player1_id, player2_id):
        self.game_id = game_id

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
        self.ball_velocity = {'x': 1, 'y': 1}
        self.is_running = True
    
    def update_ball_pos(self):
        self.ball_position['x'] += self.ball_velocity['x']
        self.ball_position['y'] += self.ball_velocity['y']

    def check_ball_wall_collision(self):
        if self.ball_position['y'] <= 0:
            self.ball_velocity['y'] = abs(self.ball_velocity['y'])
        if self.ball_position['y'] >= self.canvas['height']:
            self.ball_velocity['y'] = -abs(self.ball_velocity['y'])

    def check_ball_paddle_collision(self):
        if self.ball_position['x'] <= self.paddle['width']:
            if self.players['player1']['position']['y'] <= self.ball_position['y'] <= self.players['player1']['position']['y'] + self.paddle['height']:
                self.ball_velocity['x'] = abs(self.ball_velocity['x'])
        
        if self.ball_position['x'] >= self.canvas['width'] - self.paddle['width']:
            if self.players['player2']['position']['y'] <= self.ball_position['y'] <= self.players['player2']['position']['y'] + self.paddle['height']:
                self.ball_velocity['x'] = -abs(self.ball_velocity['x'])

    def check_score(self):
        if self.ball_position['x'] <= 0:
            self.players['player2']['score'] += 1
            self.reset_ball()
        
        if self.ball_position['x'] >= self.canvas['width']:
            self.players['player1']['score'] += 1
            self.reset_ball()

    def reset_ball(self):
        self.ball_position = {'x': self.canvas['width'] // 2, 'y': self.canvas['height'] // 2}
        self.ball_velocity = {'x': 1, 'y': 1}

    def get_player_by_id(self, user_id):
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
    
    def score_point(self, user_id):
        if user_id == self.players['player1']['id']:
            self.players['players1']['score'] += 1
        elif user_id == self.players['player2']['id']:
            self.players['players2']['score'] += 1

    def get_state(self):
        return {
            'game_id': self.game_id,
            'canvas': self.canvas,
            'paddle': self.paddle,
            'players': self.players,
            'ball_position': self.ball_position,
            'running': self.is_running
        }
    