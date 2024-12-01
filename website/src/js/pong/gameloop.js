/*
 * Game drawing loop
 */

function draw() {
    clearCanva(Game.contexts.gameCtx);

    drawPaddle(Game.contexts.gameCtx, Game.paddle.leftX, Game.paddle.leftY);
    drawPaddle(Game.contexts.gameCtx, Game.paddle.rightX, Game.paddle.rightY);

    drawBall(Game.contexts.gameCtx);
}

function gameLoop() {
    if (!Game.isRunning)
        return;
    draw();
    requestAnimationFrame(gameLoop);
    setInterval(sendPlayerMoves, 16); // 60 / s
}
