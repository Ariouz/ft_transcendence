const PONG_QUEUE_API = `${PONG_SERVICE_URL}/queue`;

let g_userInPongQueue = false;

// Todo add queue type
async function joinQueue()
{
    let url = `${PONG_QUEUE_API}/join/`;
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
        console.log(data);
        g_userInPongQueue = true;
    }).catch(error => {
        console.log(error);
    });
}

// Todo add queue type
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
        console.log(data);
        g_userInPongQueue = false;
        navigate("/pong");
    }).catch(error => {
        console.log(error);
    });
}