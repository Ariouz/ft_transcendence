/*
 * Initial game values
 */

const PONG_CANVAS_WIDTH = 800;
const PONG_CANVAS_HEIGHT = 400;

const Game = {
    canvases: {
        background: null,
        net: null,
        game: null,
    },
    contexts: {
        backgroundCtx: null,
        netCtx: null,
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

    init: function (gameType, isTournament) {
        removePreviousBackgroundImage();
        if (!this.canvases) return ;

        this.canvases.background = document.getElementById('backgroundCanvas');
        this.canvases.net = document.getElementById('netCanvas');
        this.canvases.game = document.getElementById('pongCanvas');

        this.contexts.backgroundCtx = this.canvases.background.getContext('2d');
        this.contexts.netCtx = this.canvases.net.getContext('2d');
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

        setGameBackground(gameType, isTournament);
        drawNet(this.contexts.netCtx);
    },

    startGameLoop: function (gameType, isTournament) {
        this.init(gameType, isTournament);
        gameLoop();
    },

    stopGameLoop: function () {
        this.isRunning = false;
    }
};

async function setGameBackground(gameType, isTournament) {
    if (gameType != "arcade" && !isTournament) {
        drawCanvasBackground(Game.contexts.gameCtx);
        return;
    }
    const imageUrl = getStyle('--canvas-background-url').trim().replace(/^["']|["']$/g, '');
    if (!imageUrl) {
        drawCanvasBackground(Game.contexts.gameCtx);
        return;
    }
    const isValid = await isImageValid(imageUrl);

    if (!isValid) {
        drawCanvasBackground(Game.contexts.gameCtx);
        return;
    }
    const hasSetImageBackground = setImageBackground(imageUrl);
    if (hasSetImageBackground)
        return;
    drawCanvasBackground(Game.contexts.gameCtx);
}

function isImageValid(url) {
    return new Promise((resolve) => {
        const img = new Image();
        img.onload = () => resolve(true);
        img.onerror = () => resolve(false);
        img.src = url;
    });
}

function setImageBackground(imageUrl) {
    const targetDiv = document.querySelector('.canvas_layers_container');
    if (!targetDiv)
        return false;

    const imgElement = document.createElement('img');
    imgElement.id = 'pongBackgroundImage';
    imgElement.alt = 'background';
    imgElement.src = imageUrl;

    try {
        targetDiv.insertBefore(imgElement, targetDiv.firstChild);
        return true;
    } catch (error) {
        return false;
    }
}

function removePreviousBackgroundImage() {
    const targetDiv = document.querySelector('.canvas_layers_container');
    if (!targetDiv)
        return ;
    const existingImgElement = targetDiv.querySelector('#pongBackgroundImage');
    if (existingImgElement) {
        try {
            targetDiv.removeChild(existingImgElement);
        } catch (error) {
        }
    }

}
