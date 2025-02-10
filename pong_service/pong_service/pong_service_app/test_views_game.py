from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
import json
from pong_service_app.models import PongGame

class GameViewsTestCase(TestCase):
    
    def setUp(self):
        self.test_game = PongGame.objects.create(
            game_id="test_game",
            users=[1, 2],
            status="waiting",
            type="local1v1",
            score={"1": 0, "2": 0},
            winner_id=None,
            map_theme="default",
            tournament_id=None
        )
        self.api_url = "https://testserver/api/"

    def test_get_game_data_success(self):
        url = f"{self.api_url}game/data/?game_id=test_game"
        response = self.client.get(url, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["game_id"], "test_game")

    def test_get_game_data_no_id(self):
        url = f"{self.api_url}game/data/"
        response = self.client.get(url, secure=True)
        self.assertEqual(response.status_code, 400)

    def test_get_game_data_not_found(self):
        url = f"{self.api_url}game/data/?game_id=non_existent_game"
        response = self.client.get(url, secure=True)
        self.assertEqual(response.status_code, 404)

    @patch("myapp.views.run_start_game")
    def test_start_game_success(self, mock_run_start_game):
        url = f"{self.api_url}game/start/"
        response = self.client.post(url, json.dumps({"game_id": "test_game"}), content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 200)
        mock_run_start_game.assert_called_once_with("test_game")

    def test_start_game_no_id(self):
        url = f"{self.api_url}game/start/"
        response = self.client.post(url, json.dumps({}), content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 400)

    def test_start_game_not_found(self):
        url = f"{self.api_url}game/start/"
        response = self.client.post(url, json.dumps({"game_id": "non_existent_game"}), content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 404)

    def test_create_local_game_success(self):
        url = f"{self.api_url}game/create/local/"
        response = self.client.post(url, json.dumps({"user_id": 1}), content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 200)

    def test_create_local_game_no_user_id(self):
        url = f"{self.api_url}game/create/local/"
        response = self.client.post(url, json.dumps({}), content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 400)

    def test_can_join_success(self):
        url = f"{self.api_url}game/can-join/"
        response = self.client.post(url, json.dumps({"user_id": 1, "game_id": "test_game"}), content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 200)

    def test_can_join_no_user_id(self):
        url = f"{self.api_url}game/can-join/"
        response = self.client.post(url, json.dumps({"game_id": "test_game"}), content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 400)

    def test_can_join_no_game_id(self):
        url = f"{self.api_url}game/can-join/"
        response = self.client.post(url, json.dumps({"user_id": 1}), content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 400)

    def test_can_join_game_not_found(self):
        url = f"{self.api_url}game/can-join/"
        response = self.client.post(url, json.dumps({"user_id": 1, "game_id": "non_existent_game"}), content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 404)

    def test_can_join_not_a_player(self):
        url = f"{self.api_url}game/can-join/"
        response = self.client.post(url, json.dumps({"user_id": 3, "game_id": "test_game"}), content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 403)

    def test_can_join_game_ended(self):
        self.test_game.status = "finished"
        self.test_game.save()
        url = f"{self.api_url}game/can-join/"
        response = self.client.post(url, json.dumps({"user_id": 1, "game_id": "test_game"}), content_type="application/json", secure=True)
        self.assertEqual(response.status_code, 403)
