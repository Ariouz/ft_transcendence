class PongGameState:
    def __init__(self, game_id, player1_id, player2_id):
        self.game_id = game_id
        
        self.players = {
            'player1': {
                'id': player1_id,
                'position': {'x': 0, 'y': 0},
                'score': '0'
            },
            'player2': {
                'id': player2_id,
                'position': {'x': 0, 'y': 0},
                'score': '0'
            }
        }

        self.ball_position = {'x': 0, 'y': 0}
        self.ball_velocity = {'x': 1, 'y': 1}
        self.is_running = True
    
    def update_ball_pos(self):
        self.ball_position['x'] += self.ball_velocity['x']
        self.ball_position['y'] += self.ball_velocity['y']
    
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
            'players': self.players,
            'ball_position': self.ball_position,
            'running': self.is_running
        }
    