/*
 * Game drawing loop
 */

function draw() {
    clearCanva();

    drawBackground();

    drawNet();

    drawPaddle(leftPaddleX, leftPaddleY);
    drawPaddle(rightPaddleX, rightPaddleY);

    drawBall();
    updateLeftPaddlePosition();
}

function gameLoop() {
    draw();
    requestAnimationFrame(gameLoop);
}

gameLoop();
