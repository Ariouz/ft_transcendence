// https://developer.mozilla.org/fr/docs/Web/API/WebSocket

let g_pongUserWebSocket;
let g_pongGameWebSocket;
let g_pongGamePlayerPaddle;
let g_pongGameState;

// Create WebSocket connection if user was already logged-in when opening the page
function loadPongUserWebsocket()
{
    if (g_pongUserWebSocket)
        return;
    let user_token = getCookie("session_token");
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
                    createPongGameWebSocket(game_id, user_token);
                    navigate(`/pong/game?gid=${game_id}`);
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

function createPongGameWebSocket() {
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
    
    g_pongGameWebSocket.onmessage = async function (e) {
        console.log("Pong Game WS: Message received:", e);
        try {
            const data = JSON.parse(e.data);
            g_error_pong_ws = false;
            if (data.type)
            {
                let state = data.state;
                /*
                {"type":"game_state_update","state":
                {"game_id":177,"canvas":{"width":800,"height":400},
                "paddle":{"width":10,"height":70,"speed":7},
                "players":
                {"player1":{"id":17,"position":{"x":0,"y":165},"score":0},
                "player2":{"id":12,"position":{"x":790,"y":165},"score":0}
                },
                "ball_position":{"x":600,"y":400},"running":true}}*/
                
                if (g_pongGamePlayerPaddle == undefined)
                    {
                    let userId = await retrieveId(user_token);
                    userId = userId.user_id;
                    if (state.players.player1.id == userId)
                        g_pongGamePlayerPaddle = 'player1';
                    else if (state.players.player2.id == userId)
                        g_pongGamePlayerPaddle = 'player2';
                }

                if (state.running != Game.isRunning)
                    Game.isRunning = !Game.isRunning;
                
                console.log(JSON.stringify(data));
                ball = state.ball_position;
                Game.ball.x = ball.x;
                Game.ball.y = ball.y;
                
                // TODO rendre + lisible
                if (g_pongGamePlayerPaddle == 'player1')
                    {
                    Game.paddle.leftX = state.players.player1.position.x;
                    Game.paddle.leftY = state.players.player1.position.y;
                    
                    Game.paddle.rightX = state.players.player2.position.x;
                    Game.paddle.rightY = state.players.player2.position.y;
                }
                else if (g_pongGamePlayerPaddle == 'player2')
                {
                    // Reverse paddles' sides
                    Game.paddle.leftX = state.players.player2.position.x - (Game.canvas.width - Game.paddle.width);
                    Game.paddle.leftY = state.players.player2.position.y;
                    
                    Game.paddle.rightX = state.players.player1.position.x + (Game.canvas.width - Game.paddle.width);
                    Game.paddle.rightY = state.players.player1.position.y;
                }
                
            }
            else
                g_error_pong_ws = true;
        } catch (error) {
            g_error_pong_ws = true;
        }
    };
}
