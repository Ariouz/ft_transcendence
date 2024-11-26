/*
 * Player movement
 */

lastSentTime = Date.now();
SEND_INTERVAL = 16;

function sendPlayerMoves() {
    if (Game.isPaused || !Game.isRunning) return;

    let currentTime = Date.now();
    if (currentTime - lastSentTime < SEND_INTERVAL) return;

    let moves = [];

    if (Game.controls.upPressed) {
        moves.push({
            player_paddle: g_pongGamePlayerPaddle == "both" ? "player1" : g_pongGamePlayerPaddle,
            direction: "UP"
        });
    }

    if (Game.controls.downPressed) {
        moves.push({
            player_paddle: g_pongGamePlayerPaddle == "both" ? "player1" : g_pongGamePlayerPaddle,
            direction: "DOWN"
        });
    }

    if (g_pongGameType == "local1v1") {
        if (Game.controls.upArrowPressed) {
            moves.push({
                player_paddle: "player2",
                direction: "UP"
            });
        }

        if (Game.controls.downArrowPressed) {
            moves.push({
                player_paddle: "player2",
                direction: "DOWN"
            });
        }
    }

    if (moves.length > 0) {
        g_pongGameWebSocket.send(JSON.stringify({
            type: "player_move",
            data: moves
        }));
    }

    lastSentTime = currentTime;
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

    if (e.key === Game.controls.upArrowKey.toLowerCase() || e.key === Game.controls.upArrowKey) {
        Game.controls.upArrowPressed = true;
    }
    if (e.key === Game.controls.downArrowKey.toLowerCase() || e.key === Game.controls.downArrowKey) {
        Game.controls.downArrowPressed = true;
    }
}

function keyUpHandler(e) {
    if (e.key === Game.controls.upKey.toLowerCase() || e.key === Game.controls.upKey) {
        Game.controls.upPressed = false;
    }
    if (e.key === Game.controls.downKey.toLowerCase() || e.key === Game.controls.downKey) {
        Game.controls.downPressed = false;
    }

    if (e.key === Game.controls.upArrowKey.toLowerCase() || e.key === Game.controls.upArrowKey) {
        Game.controls.upArrowPressed = false;
    }
    if (e.key === Game.controls.downArrowKey.toLowerCase() || e.key === Game.controls.downArrowKey) {
        Game.controls.downArrowPressed = false;
    }
}
