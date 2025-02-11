import json
import logging
from django.test import TestCase
from django.urls import reverse
from pong_service_app.models import PongGame, PongUser
from pong_service_app.api.themes import get_default_theme

class PongGameViewsTestCase(TestCase):
    def setUp(self):
        """Create test data"""
        self.user = PongUser.objects.create(user_id=1)
        self.game = PongGame.objects.create(
            game_id=1,
            users=[1, 2],
            winner_id=1,
            score=[{"player1": 10, "player2": 5}],
            type="1v1",
            status="ongoing",
            map_theme=get_default_theme(),
        )
    
    def test_get_game_data(self):
        """Test retrieving game data"""
        url = "https://testserver/api/game/data/?game_id=1"
        response = self.client.get(url, secure=True)
        self.assertEqual(response.status_code, 200)
    
    def test_get_game_data_no_id(self):
        """Test retrieving game data with no game_id"""
        url = "https://testserver/api/game/data/"
        response = self.client.get(url, secure=True)
        self.assertEqual(response.status_code, 400)
    
    def test_get_game_data_invalid_id(self):
        """Test retrieving game data with invalid game_id"""
        url = "https://testserver/api/game/data/?game_id=999"
        response = self.client.get(url, secure=True)
        self.assertEqual(response.status_code, 404)
    
    def test_start_game(self):
        """Test starting a game"""
        url = "https://testserver/api/game/start/"
        response = self.client.post(url, json.dumps({"game_id": 1}), content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 200)
    
    def test_start_game_no_id(self):
        """Test starting a game with no game_id"""
        url = "https://testserver/api/game/start/"
        response = self.client.post(url, json.dumps({}), content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 404)
    
    def test_start_game_invalid_id(self):
        """Test starting a game with invalid game_id"""
        url = "https://testserver/api/game/start/"
        response = self.client.post(url, json.dumps({"game_id": 999}), content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 404)
    
    def test_create_local_game(self):
        """Test creating a local game"""
        url = "https://testserver/api/game/create/local/"
        response = self.client.post(url, json.dumps({"user_id": 1}), content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 200)
    
    def test_create_local_game_no_id(self):
        """Test creating a local game with no user_id"""
        url = "https://testserver/api/game/create/local/"
        response = self.client.post(url, json.dumps({}), content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 400)
    
    # TODO
    # def test_create_local_game_not_existing_id(self):
    #     """Test creating a local game with not existing user_id"""
    #     url = "https://testserver/api/game/create/local/"
    #     response = self.client.post(url, json.dumps({"user_id": 42}), content_type="application/json", secure=True)
    #     self.assertEqual(response.status_code, 400)
        
    def test_can_join(self):
        """Test checking if a user can join a game"""
        url = "https://testserver/api/game/can-join/"
        response = self.client.post(
            url,
            json.dumps({"user_id": 1, "game_id": 1}),
            content_type="application/json",
            secure=True
        )
        self.assertEqual(response.status_code, 200)
    
    def test_can_join_invalid_game_id(self):
        """Test checking if a user can join a non-existent game"""
        url = "https://testserver/api/game/can-join/"
        response = self.client.post(
            url,
            json.dumps({"user_id": 1, "game_id": 999}),
            content_type="application/json",
            secure=True
        )
        self.assertEqual(response.status_code, 400)
    
    def test_can_join_invalid_user_id(self):
        """Test checking if a user not in the game can join"""
        url = "https://testserver/api/game/can-join/"
        response = self.client.post(
            url,
            json.dumps({"user_id": 3, "game_id": 1}),
            content_type="application/json",
            secure=True
        )
        self.assertEqual(response.status_code, 403)
    
    def test_can_join_finished_game(self):
        """Test checking if a user can join a finished game"""
        self.game.status = "finished"
        self.game.save()
        url = "https://testserver/api/game/can-join/"
        response = self.client.post(
            url,
            json.dumps({"user_id": 1, "game_id": 1}),
            content_type="application/json",
            secure=True
        )
        self.assertEqual(response.status_code, 403)
