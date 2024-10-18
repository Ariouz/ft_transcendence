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
}

function gameLoop() {
    if (!Game.isRunning)
        return;
    draw();
    requestAnimationFrame(gameLoop);
    setInterval(sendPlayerMoves, 16); // 60 / s
}
