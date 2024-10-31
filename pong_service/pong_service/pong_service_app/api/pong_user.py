from pong_service_app.models import *
import math

def create_user_if_not_exists(user_id):
    if not PongUser.objects.filter(user_id=user_id).exists():
        user = PongUser.objects.create(user_id=user_id)
        user.save()

    if not PongUserStats.objects.filter(user_id=user_id).exists():
        user_stats = PongUserStats.objects.create(user_id=user_id)
        user_stats.save()


def get_user(user_id):
    if not PongUser.objects.filter(user_id=user_id).exists():
        return create_user_if_not_exists(user_id)
    return PongUser.objects.filter(user_id=user_id).get()


def get_user_stats(user_id):
    if not PongUserStats.objects.filter(user_id=user_id).exists():
        return create_user_if_not_exists(user_id)
    return PongUserStats.objects.filter(user_id=user_id).get()


def add_game_to_history(user_id, game_id, won_game=False):
    user = get_user(user_id)
    user_stats = get_user_stats(user_id)

    if not user or not user_stats:
        create_user_if_not_exists(user_id)
    
    user.game_history.insert(0, game_id)
    user.last_game = game_id
    user_stats.played += 1
    user_stats.wins += 1 if won_game else 0
    user_stats.loses += 1 if not won_game else 0

    user.save()
    user_stats.save()


def get_win_rate(user_id):
    user_stats = get_user_stats(user_id)

    if not(user_stats):
        create_user_if_not_exists(user_id)

    if user_stats.loses <= 0: return user_stats.wins

    return round(user_stats.wins / user_stats.played, 2)


def get_user_played_games(user_id):
    user = get_user(user_id)

    if not user:
        create_user_if_not_exists(user_id)

    return user.game_history


def get_game_data(game_id):
    if not PongGame.objects.filter(game_id=game_id).exists():
        return {"error": "Game not found"}

    game = PongGame.objects.filter(game_id=game_id).get()

    return {
        "game_id": game_id,
        "players": game.users,
        "winner_id": game.winner_id,
        "score": game.score,
        "status": game.status,
        "type": game.type,
        "date": game.date
    }