/*
 * Drawing game elements
 */

function getStyle(styleName) {
    // --style-name
    return getComputedStyle(document.documentElement).getPropertyValue(styleName);
}

function drawRectangle(x, y, width, height, fillColor, strokeColor = null, strokeWidth = 0) {
    ctx.beginPath();
    ctx.rect(x, y, width, height);
    ctx.fillStyle = fillColor;
    if (strokeColor !== null && strokeWidth !== 0) {
        ctx.lineWidth = strokeWidth;
        ctx.strokeStyle = strokeColor;
    }
    ctx.fill();
    ctx.closePath();
}

function drawCircle(x, y, radius, fillColor, strokeColor = null, strokeWidth = 0) {
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

function drawNet() {
    ctx.beginPath();
    ctx.setLineDash([5, 15]);
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.strokeStyle = getStyle('--net-color');
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.closePath();
}
function drawBall() {
    drawCircle(ballX, ballY, ballRadius,
        getStyle('--ball-color')
    );
}

function drawPaddle(x, y) {
    drawRectangle(x, y, paddleWidth, paddleHeight,
        getStyle('--paddle-color'),
    );
}

function drawBackground() {
    drawRectangle(0, 0, canvas.width, canvas.height,
        getStyle('--canvas-color'),
        getStyle('--canvas-stroke-color', 8
        ));
}

function clearCanva() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}
