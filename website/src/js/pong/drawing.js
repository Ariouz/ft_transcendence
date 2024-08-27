/*
 * Drawing game elements
 */

function getStyle(styleName) {
    // --style-name
    return getComputedStyle(document.documentElement).getPropertyValue(styleName);
}

function drawRectangle(x, y, width, height, fillColor, strokeColor = null, strokeWidth = 0) {
    Game.ctx.beginPath();
    Game.ctx.rect(x, y, width, height);
    Game.ctx.fillStyle = fillColor;
    if (strokeColor !== null && strokeWidth !== 0) {
        Game.ctx.lineWidth = strokeWidth;
        Game.ctx.strokeStyle = strokeColor;
    }
    Game.ctx.fill();
    Game.ctx.closePath();
}

function drawCircle(x, y, radius, fillColor, strokeColor = null, strokeWidth = 0) {
    Game.ctx.beginPath();
    Game.ctx.arc(x, y, radius, 0, Math.PI * 2);
    Game.ctx.fillStyle = fillColor;
    if (strokeColor !== null && strokeWidth !== 0) {
        Game.ctx.lineWidth = strokeWidth;
        Game.ctx.strokeStyle = strokeColor;
    }
    Game.ctx.fill();
    Game.ctx.closePath();
}

function drawNet() {
    Game.ctx.beginPath();
    Game.ctx.setLineDash([5, 15]);
    Game.ctx.moveTo(Game.canvas.width / 2, 0);
    Game.ctx.lineTo(Game.canvas.width / 2, Game.canvas.height);
    Game.ctx.strokeStyle = getStyle('--net-color');
    Game.ctx.lineWidth = 2;
    Game.ctx.stroke();
    Game.ctx.closePath();
}
function drawBall() {
    drawCircle(Game.ball.x, Game.ball.y, Game.ball.radius,
        getStyle('--ball-color')
    );
}

function drawPaddle(x, y) {
    drawRectangle(x, y, Game.paddle.width, Game.paddle.height,
        getStyle('--paddle-color'),
    );
}

function drawBackground() {
    drawRectangle(0, 0, Game.canvas.width, Game.canvas.height,
        getStyle('--canvas-color'),
        getStyle('--canvas-stroke-color', 8
        ));
}

function clearCanva() {
    Game.ctx.clearRect(0, 0, Game.canvas.width, Game.canvas.height);
}
