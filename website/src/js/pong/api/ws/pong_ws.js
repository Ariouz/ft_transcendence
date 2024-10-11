// https://developer.mozilla.org/fr/docs/Web/API/WebSocket

let g_pongWebSocket;
let g_error_pong_ws;

// Create WebSocket connection if user was already logged-in when opening the page
function loadPongWebsocket()
{
    if (g_pongWebSocket)
        return;
    let user_token = getCookie("session_token");
    if (user_token && user_token.length > 0) {
        createWebSocketPong();
    }
}

function createWebSocketPong() {
    let user_token = getCookie("session_token");
    const WEBSOCKET_PONG_URL = `ws://localhost:7000/ws/pong/${user_token}/`;
    g_pongWebSocket = new WebSocket(WEBSOCKET_PONG_URL);
    console.log("Pong WS: Created WebSocket for user's pong.");

    g_pongWebSocket.onopen = function (e) {
        console.log("Pong WS: Opened pong websocket connection.");
    }

    g_pongWebSocket.onclose = function (e) {
        console.log("Pong WS: Closed pong websocket connection.");
    }

    g_pongWebSocket.onmessage = function (e) {
        console.log("Pong WS: Message received:", e);
        try {
            const data = JSON.parse(e.data);
            g_error_pong_ws = false;
            if (data.type)
            {
                if (data.type === "game_create")
                {
                    game_id = data.game_id;
                    console.log("Game created with id " + game_id);
                    navigate(`/pong/game/?gid=${game_id}`);
                }
            }
            else
                g_error_pong_ws = true;
        } catch (error) {
            g_error_pong_ws = true;
        }
    };
}