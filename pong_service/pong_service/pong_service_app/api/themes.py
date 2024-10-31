import random


THEMES = [
    # Thème par défaut
    {
        "--paddle-color": "#F72585",
        "--ball-color": "white",
        "--canvas-color": "#0D00A4",
        "--canvas-stroke-color": "#140152",
        "--shadow-color": "rgba(0, 0, 0, 0.5)",
        "--net-color": "#ffffff80",
    },
    # Thème vert
    {
        "--paddle-color": "#4CAF50",
        "--ball-color": "#C8E6C9",
        "--canvas-color": "#2E7D32",
        "--canvas-stroke-color": "#1B5E20",
        "--shadow-color": "rgba(0, 128, 0, 0.5)",
        "--net-color": "#ffffff80",
    },
    # Thème jaune
    {
        "--paddle-color": "#FFEB3B",
        "--ball-color": "#FFF9C4",
        "--canvas-color": "#FBC02D",
        "--canvas-stroke-color": "#F57F17",
        "--shadow-color": "rgba(255, 235, 59, 0.5)",
        "--net-color": "#ffffff80",
    },
    # Thème rouge
    {
        "--paddle-color": "#FF1744",
        "--ball-color": "#FFCDD2",
        "--canvas-color": "#D50000",
        "--canvas-stroke-color": "#B71C1C",
        "--shadow-color": "rgba(255, 23, 68, 0.5)",
        "--net-color": "#ffffff80",
    },
]


def get_random_arcade_theme():
    random_theme = random.choice(THEMES[1:])
    return random_theme


def get_default_theme():
    default_theme = THEMES[0]
    return default_theme


def get_theme(game_type):
    theme = get_default_theme()
    if game_type == "arcade":
        theme = get_random_arcade_theme()
    return theme
