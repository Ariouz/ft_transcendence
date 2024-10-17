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
                if (data.type == "game_state_update")
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
                    "ball_position":{"x":600,"y":400},
                    "running":true, "paused": false}}*/
                    
                    if (g_pongGamePlayerPaddle == undefined)
                    {
                        let userId = await retrieveId(user_token);
                        userId = userId.user_id;
                        if (state.players.player1.id == userId)
                            g_pongGamePlayerPaddle = 'player1';
                        else if (state.players.player2.id == userId)
                            g_pongGamePlayerPaddle = 'player2';
                    }

                    if (state.paused != Game.isPaused)
                        Game.isPaused = !Game.isPaused;

                    if (state.running != Game.isRunning)
                        Game.isRunning = !Game.isRunning;
                    
                    console.log(JSON.stringify(data));
                    ball = state.ball_position;
                    
                    Game.ball.y = ball.y;

                    
                    // TODO rendre + lisible
                    if (g_pongGamePlayerPaddle == 'player1')
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
                        // Reverse paddles' sides
                        Game.paddle.leftX = state.players.player2.position.x - (Game.canvas.width - Game.paddle.width);
                        Game.paddle.leftY = state.players.player2.position.y;
                        
                        Game.paddle.rightX = state.players.player1.position.x + (Game.canvas.width - Game.paddle.width);
                        Game.paddle.rightY = state.players.player1.position.y;
                    }
                }
                else if (data.type == "game_player_scored")
                {
                    /*"type": "game_player_scored",
                    "state": game_data,
                    "scoring_player": scoring_player,
                    "countdown_timer": ball_timer
                    */
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
            }
            else
                g_error_pong_ws = true;
        } catch (error) {
            g_error_pong_ws = true;
        }
    };
}


function updateScore(game_data, data)
{
    pong_self_score = document.getElementById("pong_self_score");
    pong_opponent_score = document.getElementById("pong_opponent_score");

    player1_score = game_data.players.player1.score;
    player2_score = game_data.players.player2.score;

    if (g_pongGamePlayerPaddle == 'player1')
    {
        pong_self_score.innerText = player1_score;
        pong_opponent_score.innerText = player2_score;
    }
    else
    {
        pong_self_score.innerText = player2_score;
        pong_opponent_score.innerText = player1_score;
    }

    console.log(game_data);

    pong_text_overlay = document.getElementById("pong_text_overlay");

    countdown_timer = data.countdown_timer;
    scorer = data.scoring_player;

    txt_time = countdown_timer - 3 - 1;
    pong_text_overlay.innerText = scorer + " scored!";
    pong_text_overlay.classList.add("pong_text_overlay_shown");

    countdown_timer = 4;
    let timer = setInterval(() => {
        if (countdown_timer <= 0)
        {
            pong_text_overlay.classList.remove("pong_text_overlay_shown");
            pong_text_overlay.innerText = "";
            clearInterval(timer);
        }

        if (txt_time > 0)
            txt_time--;
        else
            pong_text_overlay.innerText = countdown_timer;

        countdown_timer--;
    }, 1000);

}

function startTimer(countdown_timer)
{
    pong_text_overlay = document.getElementById("pong_text_overlay");

    txt_time = countdown_timer - 3 - 1;
    pong_text_overlay.innerText = "Starting in...";
    pong_text_overlay.classList.add("pong_text_overlay_shown");

    countdown_timer = 4;
    let timer = setInterval(() => {
        if (countdown_timer <= 0)
        {
            pong_text_overlay.classList.remove("pong_text_overlay_shown");
            pong_text_overlay.innerText = "";
            clearInterval(timer);
        }

        if (txt_time > 0)
            txt_time--;
        else
            pong_text_overlay.innerText = countdown_timer;

        countdown_timer--;
    }, 1000);
}

function winnerTimer(countdown_timer, winner, game_data)
{
    pong_self_score = document.getElementById("pong_self_score");
    pong_opponent_score = document.getElementById("pong_opponent_score");

    player1_score = game_data.players.player1.score;
    player2_score = game_data.players.player2.score;

    if (g_pongGamePlayerPaddle == 'player1')
    {
        pong_self_score.innerText = player1_score;
        pong_opponent_score.innerText = player2_score;
    }
    else
    {
        pong_self_score.innerText = player2_score;
        pong_opponent_score.innerText = player1_score;
    }


    pong_text_overlay = document.getElementById("pong_text_overlay");

    pong_text_overlay.innerText = winner + " won the game!";
    pong_text_overlay.classList.add("pong_text_overlay_shown");

    let timer = setInterval(() => {
        if (countdown_timer <= 0)
        {
            pong_text_overlay.classList.remove("pong_text_overlay_shown");
            pong_text_overlay.innerText = "";
            clearInterval(timer);

            g_pongGameWebSocket.close();
            g_pongGameState = null;
            g_pongGamePlayerPaddle = null;
            navigate("/pong");
        }

        countdown_timer--;
    }, 1000);
}