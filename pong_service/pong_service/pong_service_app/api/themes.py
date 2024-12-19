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
        "--net-color": "#ffffffC0",
        "--canvas-background-url": "/assets/images/bangkok-pink-blue.jpg",
        "--border-animation-primary-color": "#cb518a",
        "--border-animation-secondary-color": "#2068be"
    },
    {
        "--paddle-color": "#4f89c5",
        "--ball-color": "#b2d1e5",
        "--net-color": "#ffffffC0",
        "--canvas-background-url": "/assets/images/lagoon-blue-green.jpg",
        "--border-animation-primary-color": "#89e5c7",
        "--border-animation-secondary-color": "#6ec0cb"
    },
    {
        "--paddle-color": "#6e93a4",
        "--ball-color": "#db5414",
        "--net-color": "#ac9c8cC0",
        "--canvas-background-url": "/assets/images/japan-orange-blue.jpg",
        "--border-animation-primary-color": "#e3c2c0",
        "--border-animation-secondary-color": "#7ca0b0"
    },
    {
        "--paddle-color": "#a2a49c",
        "--ball-color": "#8a7f76",
        "--net-color": "#727472C0",
        "--canvas-background-url": "/assets/images/paris-gray-white.jpg",
        "--border-animation-primary-color": "#d3c7c0",
        "--border-animation-secondary-color": "#9d99a5"
    },
    {
        "--paddle-color": "#447043",
        "--ball-color": "#749a68",
        "--net-color": "#122622C0",
        "--canvas-background-url": "/assets/images/jungle-green-dark-green.jpg",
        "--border-animation-primary-color": "#194a2a",
        "--border-animation-secondary-color": "#bbc495"
    },
    {
        "--paddle-color": "#bc906f",
        "--ball-color": "#c1997f",
        "--net-color": "#8b4927C0",
        "--canvas-background-url": "/assets/images/desert-orange-white.jpg",
        "--border-animation-primary-color": "#a86038",
        "--border-animation-secondary-color": "#dabda4"
    },
    {
        "--paddle-color": "#4b3da4",
        "--ball-color": "#23a63e",
        "--net-color": "#b079b1C0",
        "--canvas-background-url": "/assets/images/candies-pink-red.jpg",
        "--border-animation-primary-color": "#d84576",
        "--border-animation-secondary-color": "#c7983f"
    },
    {
        "--paddle-color": "#225a8f",
        "--ball-color": "#613c4c",
        "--net-color": "#173546C0",
        "--canvas-background-url": "/assets/images/japan-blue-yellow.jpg",
        "--border-animation-primary-color": "#2b7eb9",
        "--border-animation-secondary-color": "#d2ad85"
    },
    {
        "--paddle-color": "#2b705b",
        "--ball-color": "#2e8e60",
        "--net-color": "#0c3517C0",
        "--canvas-background-url": "/assets/images/pond-turquoise-green.jpg",
        "--border-animation-primary-color": "#13513e",
        "--border-animation-secondary-color": "#45b055"
    },
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
