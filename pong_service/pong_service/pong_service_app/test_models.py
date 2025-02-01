from django.test import TestCase
from django.utils import timezone
from pong_service_app.models import PongUser, PongGame, PongUserStats
from pong_service_app.api.themes import get_default_theme

class PongUserModelTestCase(TestCase):
    def setUp(self):
        """Create a test PongUser"""
        self.user = PongUser.objects.create(
            user_id=1,
            game_history=[{"game_id": 1, "result": "win"}],
            last_game=5
        )

    def test_pong_user_creation(self):
        """Test that a PongUser is created correctly"""
        self.assertEqual(self.user.user_id, 1)
        self.assertEqual(self.user.game_history, [{"game_id": 1, "result": "win"}])
        self.assertEqual(self.user.last_game, 5)

    def test_pong_user_default_values(self):
        """Test default values for PongUser"""
        user = PongUser.objects.create(user_id=2)
        self.assertEqual(user.game_history, [])
        self.assertEqual(user.last_game, -1)

    def test_pong_user_str(self):
        """Test __str__ method"""
        self.assertEqual(str(self.user), "1")


class PongGameModelTestCase(TestCase):
    def setUp(self):
        """Create a test PongGame"""
        self.game = PongGame.objects.create(
            users=[1, 2],
            winner_id=1,
            score=[{"player1": 10, "player2": 5}],
            type="1v1",
            status="finished",
            date=timezone.now(),
            map_theme=get_default_theme(),
        )

    def test_pong_game_creation(self):
        """Test that a PongGame is created correctly"""
        self.assertEqual(self.game.users, [1, 2])
        self.assertEqual(self.game.winner_id, 1)
        self.assertEqual(self.game.score, [{"player1": 10, "player2": 5}])
        self.assertEqual(self.game.type, "1v1")
        self.assertEqual(self.game.status, "finished")

    def test_pong_game_default_values(self):
        """Test default values for PongGame"""
        game = PongGame.objects.create()
        self.assertEqual(game.users, [])
        self.assertEqual(game.winner_id, -1)
        self.assertEqual(game.score, [])
        self.assertEqual(game.type, "1v1")
        self.assertEqual(game.status, "init")
        self.assertEqual(game.map_theme, get_default_theme())

    def test_pong_game_str(self):
        """Test __str__ method"""
        self.assertEqual(str(self.game), str(self.game.game_id))


class PongUserStatsModelTestCase(TestCase):
    def setUp(self):
        """Create a test PongUserStats"""
        self.stats = PongUserStats.objects.create(
            user_id=1,
            played=10,
            wins=7,
            loses=3
        )

    def test_pong_user_stats_creation(self):
        """Test that PongUserStats is created correctly"""
        self.assertEqual(self.stats.user_id, 1)
        self.assertEqual(self.stats.played, 10)
        self.assertEqual(self.stats.wins, 7)
        self.assertEqual(self.stats.loses, 3)

    def test_pong_user_stats_default_values(self):
        """Test default values for PongUserStats"""
        stats = PongUserStats.objects.create(user_id=2)
        self.assertEqual(stats.played, 0)
        self.assertEqual(stats.wins, 0)
        self.assertEqual(stats.loses, 0)

    def test_pong_user_stats_str(self):
        """Test __str__ method"""
        self.assertEqual(str(self.stats), "1")
