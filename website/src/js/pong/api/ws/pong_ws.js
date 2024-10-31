// https://developer.mozilla.org/fr/docs/Web/API/WebSocket

let g_pongUserWebSocket;
let g_pongGameWebSocket;
let g_pongGamePlayerPaddle;
let g_pongGameType;

let g_pongGameOpponentDisconnected = false;
let g_pongGameInterval;

// Create WebSocket connection if user was already logged-in when opening the page
function loadPongUserWebsocket()
{
    if (g_pongUserWebSocket)
        return;
    user_token = getCookie("session_token");
    if (user_token && user_token.length > 0) {
        createPongUserWebSocket();
    }
}

function createPongUserWebSocket() {
    let user_token = getCookie("session_token");
    const WEBSOCKET_PONG_URL = `ws://localhost:7000/ws/pong/user/${user_token}/`;
    g_pongUserWebSocket = new WebSocket(WEBSOCKET_PONG_URL);
    console.log("Pong WS: Created WebSocket for user's pong.");
    
    g_pongUserWebSocket.onopen = function (e) {
        console.log("Pong WS: Opened pong websocket connection.");
    }
    
    g_pongUserWebSocket.onclose = function (e) {
        console.log("Pong WS: Closed pong websocket connection.");
    }
    
    g_pongUserWebSocket.onmessage = function (e) {
        console.log("Pong WS: Message received:", e);
        try {
            const data = JSON.parse(e.data);
            g_error_pong_ws = false;
            if (data.type)
            {
                if (data.type === "game_create")
                {
                    game_id = data.game_id;
                    g_userInPongQueue = false;
                    navigate(`/pong/game?gid=${game_id}`);
                    createPongGameWebSocket(game_id, user_token);
                }
                else {
                    console.log(JSON.stringify(data));
                }
            }
            else
                g_error_pong_ws = true;
        } catch (error) {
            g_error_pong_ws = true;
        }
    };
}

function createPongGameWebSocket(game_id) {
    if (g_pongGameWebSocket) return ;
    
    let user_token = getCookie("session_token");
    const WEBSOCKET_PONG_URL = `ws://localhost:7000/ws/pong/game/${user_token}/${game_id}/`;
    g_pongGameWebSocket = new WebSocket(WEBSOCKET_PONG_URL);
    console.log("Pong Game WS: Created WebSocket for user's pong.");
    
    g_pongGameWebSocket.onopen = function (e) {
        console.log("Pong Game WS: Opened pong websocket connection.");
    }
    
    g_pongGameWebSocket.onclose = function (e) {
        console.log("Pong Game WS: Closed pong websocket connection.");
    }
    
    g_pongGameWebSocket.onmessage = function (e) {
        handlePongGameWs(e, user_token);
    }
}


async function handlePongGameWs(e, user_token) {
    try {
        const data = JSON.parse(e.data);
        g_error_pong_ws = false;
        if (data.type)
        {
            if (data.type == "game_state_update")
                await handleGameStateUpdate(data, user_token);
            else stopInterval();
            
            if (data.type == "game_player_scored")
            {
                let state = data.state;
                updateScore(state, data);
            }
            else if (data.type == "game_start_timer")
            {
                let timer = data.countdown_timer;
                startTimer(timer);
            }
            else if (data.type == "game_winner_timer")
            {
                let state = data.state;
                let timer = data.countdown_timer;
                let winner = data.winner;
                winnerTimer(timer, winner, state);
            }
            else if (data.type == "game_user_disconnected")
            {
                let state = data.state;
                let player = data.player;
                let timer = data.countdown_timer;
                g_pongGameOpponentDisconnected = true;
                pauseTimer(timer, player, state);
            }
            else if (data.type == "game_user_reconnected")
            {
                let state = data.state;
                let player = data.player;
                let timer = data.countdown_timer;
                g_pongGameOpponentDisconnected = false;
                resumeTimer(timer, player, state);
            }
        }
        else
            g_error_pong_ws = true;
    } catch (error) {
        g_error_pong_ws = true;
    }
};

async function handleGameStateUpdate(data, user_token) {
    let state = data.state;
    if (g_pongGameType == undefined) g_pongGameType = state.game_type;
    
    await defineUserPaddle(state, user_token);
    
    if (state.paused != Game.isPaused)
        Game.isPaused = !Game.isPaused;
    
    if (state.running != Game.isRunning)
        Game.isRunning = !Game.isRunning;
    
    ball = state.ball_position;
    
    Game.ball.y = ball.y;
    movePaddles(state);
}

async function defineUserPaddle(state, user_token)
{
    if (g_pongGamePlayerPaddle != undefined)
        return ;

    if (g_pongGameType == "local1v1")
    {
        g_pongGamePlayerPaddle = "both";
        return ;
    }

    let userId = await retrieveId(user_token);
    userId = userId.user_id;
    if (state.players.player1.id == userId)
        g_pongGamePlayerPaddle = 'player1';
    else if (state.players.player2.id == userId)
        g_pongGamePlayerPaddle = 'player2';
}

function movePaddles(state)
{
    if (g_pongGamePlayerPaddle == 'player1' || g_pongGamePlayerPaddle == 'both')
    {
        Game.ball.x = ball.x;
        Game.paddle.leftX = state.players.player1.position.x;
        Game.paddle.leftY = state.players.player1.position.y;
        
        Game.paddle.rightX = state.players.player2.position.x;
        Game.paddle.rightY = state.players.player2.position.y;
    }
    else if (g_pongGamePlayerPaddle == 'player2')
    {
        Game.ball.x = Game.canvas.width - ball.x;
        Game.paddle.leftX = state.players.player2.position.x - (Game.canvas.width - Game.paddle.width);
        Game.paddle.leftY = state.players.player2.position.y;
        
        Game.paddle.rightX = state.players.player1.position.x + (Game.canvas.width - Game.paddle.width);
        Game.paddle.rightY = state.players.player1.position.y;
    }
}