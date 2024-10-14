// https://developer.mozilla.org/fr/docs/Web/API/WebSocket

let g_pongUserWebSocket;
let g_pongGameWebSocket;

let g_error_pong_ws;

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
    g_pongUserWebSocket = new WebSocket(WEBSOCKET_PONG_URL);
    console.log("Pong Game WS: Created WebSocket for user's pong.");
    
    g_pongUserWebSocket.onopen = function (e) {
        console.log("Pong Game WS: Opened pong websocket connection.");
    }
    
    g_pongUserWebSocket.onclose = function (e) {
        console.log("Pong Game WS: Closed pong websocket connection.");
    }
    
    g_pongUserWebSocket.onmessage = function (e) {
        console.log("Pong Game WS: Message received:", e);
        try {
            const data = JSON.parse(e.data);
            g_error_pong_ws = false;
            if (data.type)
            {
                console.log(JSON.stringify(data));
            }
            else
            g_error_pong_ws = true;
        } catch (error) {
            g_error_pong_ws = true;
        }
    };
}
