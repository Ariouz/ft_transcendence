/*
 * Game drawing loop
 */

function draw() {
    clearCanva();

    drawBackground();

    drawNet();

    drawPaddle(Game.paddle.leftX, Game.paddle.leftY);
    drawPaddle(Game.paddle.rightX, Game.paddle.rightY);

    drawBall();
    updateLeftPaddlePosition();
}

function gameLoop() {
    if (!Game.isRunning)
        return;
    draw();
    requestAnimationFrame(gameLoop);
}
