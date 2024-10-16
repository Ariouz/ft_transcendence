/*
 * Player movement
 */

function updateLeftPaddlePosition() {
    if (Game.isPaused || !Game.isRunning) return;
    if (Game.controls.downPressed && Game.controls.upPressed) return;

    if (Game.controls.upPressed) {
        // Game.paddle.leftY = Math.max(Game.paddle.leftY - Game.paddle.speed, 0);
        g_pongGameWebSocket.send(JSON.stringify({
            type: "player_move",
            data: {
                player_paddle: g_pongGamePlayerPaddle,
                direction: "UP"
            }
        }));
    }
    if (Game.controls.downPressed) {
        // Game.paddle.leftY = Math.min(Game.paddle.leftY + Game.paddle.speed, Game.canvas.height - Game.paddle.height);
        g_pongGameWebSocket.send(JSON.stringify({
            type: "player_move",
            data: {
                player_paddle: g_pongGamePlayerPaddle,
                direction: "DOWN"
            }
        }));
    }
}

document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);

function keyDownHandler(e) {
    if (e.key === Game.controls.upKey.toLowerCase() || e.key === Game.controls.upKey) {
        Game.controls.upPressed = true;
    }
    if (e.key === Game.controls.downKey.toLowerCase() || e.key === Game.controls.downKey) {
        Game.controls.downPressed = true;
    }
}

function keyUpHandler(e) {
    if (e.key === Game.controls.upKey.toLowerCase() || e.key === Game.controls.upKey) {
        Game.controls.upPressed = false;
    }
    if (e.key === Game.controls.downKey.toLowerCase() || e.key === Game.controls.downKey) {
        Game.controls.downPressed = false;
    }
}
