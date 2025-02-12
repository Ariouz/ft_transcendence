let g_tournamentUserWebSocket;
let g_tournamentWebSocket;
let g_error_tournament_ws;
let g_TournamentTranslations = {};

// Create WebSocket connection if user was already logged-in when opening the page
function loadTournamentUserWebsocket()
{
    if (g_tournamentUserWebSocket)
        return;
    user_token = getCookie("session_token");
    if (user_token && user_token.length > 0) {
        createTournamentUserWebSocket();
    }
}

function createTournamentUserWebSocket() {
    let user_token = getCookie("session_token");
    const WEBSOCKET_PONG_URL = `wss://${g_host}:7000/ws/tournament/user/${user_token}/`;
    g_tournamentUserWebSocket = new WebSocket(WEBSOCKET_PONG_URL);
    
    g_tournamentUserWebSocket.onopen = function (e) {
    }
    
    g_tournamentUserWebSocket.onclose = function (e) {
    }
    
    g_tournamentUserWebSocket.onmessage = function (e) {
        try {
            const data = JSON.parse(e.data);
            g_error_tournament_ws = false;
            if (data.type)
                {
                if (data.type === "joined_tournament")
                {
                    if (g_tournamentWebSocket) return ;
                    tournament_id = data.tournament_id;
                    navigate(`/tournament/lobby?tid=${tournament_id}`);
                }
                else if (data.type == "ws_connect_user")
                {
                    createTournamentWebSocket(tournament_id, user_token);
                }
                else {
                }
            }
            else
            g_error_tournament_ws = true;
        } catch (error) {
            g_error_tournament_ws = true;
        }
    };
}

function createTournamentWebSocket(tournament_id, user_token) {
    if (g_tournamentWebSocket) return ;
    
    const WEBSOCKET_PONG_URL = `wss://${g_host}:7000/ws/tournament/tournament/${user_token}/${tournament_id}/`;
    g_tournamentWebSocket = new WebSocket(WEBSOCKET_PONG_URL);
    
    g_tournamentWebSocket.onopen = function (e) {
    }
    
    g_tournamentWebSocket.onclose = function (e) {
    }
    
    g_tournamentWebSocket.onmessage = function (e) {
        handleTournamentWs(e, user_token);
    }
}
