/*
 * Player movement
 */

function updateLeftPaddlePosition() {
    if (upPressed) {
        leftPaddleY = Math.max(leftPaddleY - paddleSpeed, 0);
    }
    if (downPressed) {
        leftPaddleY = Math.min(leftPaddleY + paddleSpeed, canvas.height - paddleHeight);
    }
}

document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);

function keyDownHandler(e) {
    if (e.key === upKey.toLowerCase() || e.key === upKey) {
        upPressed = true;
    }
    if (e.key === downKey.toLowerCase() || e.key === downKey) {
        downPressed = true;
    }
}

function keyUpHandler(e) {
    if (e.key === upKey.toLowerCase() || e.key === upKey) {
        upPressed = false;
    }
    if (e.key === downKey.toLowerCase() || e.key === downKey) {
        downPressed = false;
    }
}
