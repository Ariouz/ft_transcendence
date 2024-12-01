/*
 * Initial game values
 */

const PONG_CANVAS_WIDTH = 800;
const PONG_CANVAS_HEIGHT = 400;

const Game = {
    canvases: {
        background: null,
        net: null,
        stroke: null,
        game: null,
    },
    contexts: {
        backgroundCtx: null,
        netCtx: null,
        strokeCtx: null,
        gameCtx: null,
    },
    isPaused: null,
    isRunning: null,

    paddle: {
        height: 75,
        width: 10,
        leftX: 0,
        rightX: 0,
        leftY: 0,
        rightY: 0,
        speed: 7,
    },

    ball: {
        radius: 10,
        x: 0,
        y: 0,
    },

    controls: {
        upPressed: false,
        downPressed: false,
        upKey: 'W',
        downKey: 'S',
        upArrowKey: 'ArrowUp',
        downArrowKey: 'ArrowDown',
        upArrowPressed: false,
        downArrowPressed: false,
    },

    init: function () {
        this.canvases.background = document.getElementById('backgroundCanvas');
        this.canvases.net = document.getElementById('netCanvas');
        this.canvases.stroke = document.getElementById('strokeCanvas');
        this.canvases.game = document.getElementById('pongCanvas');

        this.contexts.backgroundCtx = this.canvases.background.getContext('2d');
        this.contexts.netCtx = this.canvases.net.getContext('2d');
        this.contexts.strokeCtx = this.canvases.stroke.getContext('2d');
        this.contexts.gameCtx = this.canvases.game.getContext('2d');

        Object.values(this.canvases).forEach(canvas => {
            canvas.width = PONG_CANVAS_WIDTH;
            canvas.height = PONG_CANVAS_HEIGHT;
        });

        this.paddle.rightX = PONG_CANVAS_WIDTH - this.paddle.width;
        this.paddle.leftY = (PONG_CANVAS_HEIGHT - this.paddle.height) / 2;
        this.paddle.rightY = (PONG_CANVAS_HEIGHT - this.paddle.height) / 2;
        this.ball.x = PONG_CANVAS_WIDTH / 2;
        this.ball.y = PONG_CANVAS_HEIGHT / 2;

        this.isPaused = false;
        this.isRunning = true;

        // TODO: setWebsiteBackgroundColor(getStyle('--flashy-pink'));

        // TODO: draw background when no image

        drawNet(this.contexts.netCtx);
    },

    startGameLoop: function () {
        this.init();
        gameLoop();
    },

    stopGameLoop: function () {
        this.isRunning = false;
    }
};
