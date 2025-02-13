/*
 * Drawing game elements
 */

function getStyle(styleName) {
    // --style-name
    return getComputedStyle(document.documentElement).getPropertyValue(styleName);
}

function drawRectangle(ctx, x, y, width, height, fillColor = null) {
    ctx.beginPath();
    ctx.rect(x, y, width, height);
    if (fillColor != null)
        ctx.fillStyle = fillColor;
    ctx.fill();
    ctx.closePath();
}

function drawCircle(ctx, x, y, radius, fillColor, strokeColor = null, strokeWidth = 0) {
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fillStyle = fillColor;
    if (strokeColor !== null && strokeWidth !== 0) {
        ctx.lineWidth = strokeWidth;
        ctx.strokeStyle = strokeColor;
    }
    ctx.fill();
    ctx.closePath();
}

function drawNet(ctx) {
    ctx.beginPath();
    ctx.setLineDash([5, 15]);
    ctx.moveTo(PONG_CANVAS_WIDTH / 2, 0);
    ctx.lineTo(PONG_CANVAS_WIDTH / 2, PONG_CANVAS_HEIGHT);
    ctx.strokeStyle = getStyle('--net-color');
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.closePath();
}
function drawBall(ctx) {
    drawCircle(ctx, Game.ball.x, Game.ball.y, Game.ball.radius,
        getStyle('--ball-color')
    );
}

function drawPaddle(ctx, x, y) {
    drawRectangle(ctx, x, y, Game.paddle.width, Game.paddle.height,
        getStyle('--paddle-color'),
    );
}

function drawCanvasBackground(ctx) {
    drawRectangle(ctx, 0, 0, PONG_CANVAS_WIDTH, PONG_CANVAS_HEIGHT);
}

function clearCanva(ctx) {
    ctx.clearRect(0, 0, PONG_CANVAS_WIDTH, PONG_CANVAS_HEIGHT);
}
