/*
 * Game drawing loop
 */
var MALUS_FLICKER = true;
var MALUS_FLICKER_DURATION = 1;
var MALUS_FLICKER_BALL_IS_DISPLAYED = false;

var MALUS_FLICKER_START_DATE = 0;
var MALUS_FLICKER_MALUS_END_DATE = 0;
var MALUS_FLICKER_LAST_DATE_CHANGED_DISPLAY = 0;

function draw() {
    clearCanva(Game.contexts.gameCtx);

    drawPaddle(Game.contexts.gameCtx, Game.paddle.leftX, Game.paddle.leftY);
    drawPaddle(Game.contexts.gameCtx, Game.paddle.rightX, Game.paddle.rightY);

    isInMalusInterval();

    if (MALUS_FLICKER && MALUS_FLICKER_BALL_IS_DISPLAYED) {
        drawBall(Game.contexts.gameCtx);
    } else if (!MALUS_FLICKER)
        drawBall(Game.contexts.gameCtx);
    }

function gameLoop() {
    if (!Game.isRunning)
        return;
    draw();
    requestAnimationFrame(gameLoop);
    setInterval(sendPlayerMoves, 16); // 60 / s
}

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

function isInMalusInterval() {
    const currentTime = new Date();

    if (currentTime.getTime() > MALUS_FLICKER_MALUS_END_DATE.getTime())
    {
        MALUS_FLICKER = false;
        return ;
    }
    if (currentTime.getTime() > MALUS_FLICKER_LAST_DATE_CHANGED_DISPLAY.getTime()) {
        MALUS_FLICKER_LAST_DATE_CHANGED_DISPLAY = addSecondsToDate(MALUS_FLICKER_LAST_DATE_CHANGED_DISPLAY, MALUS_FLICKER_DURATION);
        MALUS_FLICKER_BALL_IS_DISPLAYED = !MALUS_FLICKER_BALL_IS_DISPLAYED;
    }

}


function addSecondsToDate(date, secondsToAdd) {
    const newDate = new Date(date);
    newDate.setSeconds(newDate.getSeconds() + secondsToAdd);
    return newDate;
}

// TODO use this function to set the flicker malus
function setFlickerMalus(malusFlickerDuration) {
    MALUS_FLICKER = true;

    MALUS_FLICKER_START_DATE = new Date();

    MALUS_FLICKER_LAST_DATE_CHANGED_DISPLAY = new Date();
    MALUS_FLICKER_LAST_DATE_CHANGED_DISPLAY = addSecondsToDate(MALUS_FLICKER_LAST_DATE_CHANGED_DISPLAY, MALUS_FLICKER_DURATION);

    MALUS_FLICKER_MALUS_END_DATE = new Date();
    MALUS_FLICKER_MALUS_END_DATE = addSecondsToDate(MALUS_FLICKER_MALUS_END_DATE, malusFlickerDuration);

    MALUS_FLICKER_BALL_IS_DISPLAYED = true;
}
