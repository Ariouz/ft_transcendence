const PONG_QUEUE_API = `${PONG_SERVICE_URL}/queue`;
const PONG_GAME_API = `${PONG_SERVICE_URL}/game`;

let g_userInPongQueue = false;
var g_matchmakingGameType = null;

async function joinQueue()
{
    let url = `${PONG_QUEUE_API}/join/`;
    let sessionToken = getCookie("session_token");
    if (sessionToken == undefined) return;

    if (!g_matchmakingGameType)
    {
        navigate('/pong');
        return ;
    }

    let userId = await retrieveId(sessionToken);
    let requestData = { user_id: userId.user_id, game_type: g_matchmakingGameType };

    postWithCsrfToken(url, requestData, true)
    .then(data => {
        if (data.success)
            g_userInPongQueue = true;
        else
            navigate('/pong');
    }).catch(async error => {
        navigate("/pong");
    });
}

async function leaveMatchmakingQueue()
{
    let url = `${PONG_QUEUE_API}/leave/`;
    let sessionToken = getCookie("session_token");

    if (sessionToken == undefined) return;
    if (!g_userInPongQueue) return;
    if (!g_matchmakingGameType) return ;

    let userId = await retrieveId(sessionToken);
    let requestData = { user_id: userId.user_id, game_type: g_matchmakingGameType };

    g_matchmakingGameType = null;

    postWithCsrfToken(url, requestData, true)
    .then(data => {
        g_userInPongQueue = false;
        navigate("/pong");
    }).catch(error => {
        navigate("/pong");
    });
}

async function createLocalGame()
{
    let sessionToken = getCookie("session_token");

    if (sessionToken == undefined)
    {
        navigate("/login");
        return ;
    }

    let url = `${PONG_GAME_API}/create/local/`;

    let userId = await retrieveId(sessionToken);
    let requestData = { user_id: userId.user_id };

    postWithCsrfToken(url, requestData, true)
    .then(data => {
        g_userInPongQueue = false;
    }).catch(async error => {
        await showUnavailableError();
        navigate("/pong");
    });
}