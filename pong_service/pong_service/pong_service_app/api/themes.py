import random


THEMES = [
    {
        "--paddle-color": "#48dbfb",
        "--ball-color": "#0abde3",
        "--net-color": "#ffffff80",
        "--canvas-background-url": "/assets/images/grece-blue-white.jpg",
        "--border-animation-primary-color": "#63acd3",
        "--border-animation-secondary-color": "#e8ebef"
    },
    {
        "--paddle-color": "#3f81d0",
        "--ball-color": "#e36da4",
        "--net-color": "#ffffff80",
        "--canvas-background-url": "/assets/images/bangkok-pink-blue.jpg",
        "--border-animation-primary-color": "#cb518a",
        "--border-animation-secondary-color": "#2068be"
    }
]


def get_random_arcade_theme():
    random_theme = random.choice(THEMES)
    return random_theme


def get_default_theme():
    default_theme = {}
    return default_theme


def get_theme(game_type):
    theme = get_default_theme()
    if game_type == "arcade":
        theme = get_random_arcade_theme()
    return theme
