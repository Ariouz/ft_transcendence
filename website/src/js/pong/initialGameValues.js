/*
 * Initial game values
 */

const Game = {
    canvas: null,
    ctx: null,
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
        this.canvas = document.getElementById('pongCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.paddle.rightX = this.canvas.width - this.paddle.width;
        this.paddle.leftY = (this.canvas.height - this.paddle.height) / 2;
        this.paddle.rightY = (this.canvas.height - this.paddle.height) / 2;
        this.ball.x = this.canvas.width / 2;
        this.ball.y = this.canvas.height / 2;
        this.isPaused = false;
        this.isRunning = true;
    },

    // TODO Temporary. This will normally be replaced by game management via the back end.
    startGameLoop: function () {
        Game.init();
        gameLoop();
    },

    // TODO Temporary. This will normally be replaced by game management via the back end.
    stopGameLoop: function () {
        this.isRunning = false;
    }
};
