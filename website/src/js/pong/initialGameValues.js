/*
 * Initial game values
 */

// Paddle
const paddleHeight = 75;
const paddleWidth = 10;

const leftPaddleX = 0;
const rightPaddleX = canvas.width - paddleWidth;

let leftPaddleY = (canvas.height - paddleHeight) / 2;
let rightPaddleY = (canvas.height - paddleHeight) / 2;

const paddleSpeed = 7;

// Ball
const ballRadius = 10;
let ballX = canvas.width / 2;
let ballY = canvas.height / 2;

// Player movement
let upPressed = false;
let downPressed = false;
let upKey = 'W';
let downKey = 'S';
