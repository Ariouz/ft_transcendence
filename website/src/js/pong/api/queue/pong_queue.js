const PONG_QUEUE_API = `${PONG_SERVICE_URL}/queue`;
const PONG_GAME_API = `${PONG_SERVICE_URL}/game`;

let g_userInPongQueue = false;

async function joinQueue(gameType)
{
    let url = `${PONG_QUEUE_API}/join/`;
    let sessionToken = getCookie("session_token");
    if (sessionToken == undefined) return;

    if (!gameType)
    {
        navigate('/pong');
        return ;
    }

    let userId = await retrieveId(sessionToken);
    let requestData = { user_id: userId.user_id, game_type: gameType };

    data = fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
    }).then(data => data.json())
    .then(data => {
        console.log(data);
        if (data.success)
            g_userInPongQueue = true;
        else
            navigate('/pong');
    }).catch(error => {
        console.log(error);
        navigate("/pong");
    });
}

async function leaveMatchmakingQueue()
{
    let url = `${PONG_QUEUE_API}/leave/`;
    let sessionToken = getCookie("session_token");

    if (sessionToken == undefined) return;
    if (!g_userInPongQueue) return;

    let userId = await retrieveId(sessionToken);
    console.log(userId.user_id);
    let requestData = { user_id: userId.user_id };

    data = fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
    }).then(data => data.json())
    .then(data => {
        g_userInPongQueue = false;
        navigate("/pong");
    }).catch(error => {
        console.log(error);
        navigate("/pong");
    });
}

async function createLocalGame()
{
    let url = `${PONG_GAME_API}/create/local/`;
    let sessionToken = getCookie("session_token");
    if (sessionToken == undefined) return;

    let userId = await retrieveId(sessionToken);
    console.log(userId.user_id);
    let requestData = { user_id: userId.user_id };

    data = fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
    }).then(data => data.json())
    .then(data => {
        g_userInPongQueue = false;
    }).catch(error => {
        console.log(error);
        navigate("/pong");
    });
}