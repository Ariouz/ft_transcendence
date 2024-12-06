async function isOnline(user_id)
{
    data = await fetchBack(`${USERS_SERVICE_URL}/user/online-status/get/${user_id}/`);
    return data;
}

async function setRightStatus(circleId, radarId, user_id)
{
    let circle = document.getElementById(circleId);
    let radar = document.getElementById(radarId);

    while (!g_friendListWebSocket) {
        await new Promise(resolve => setTimeout(resolve, 100));
    }

    let online = await isOnline(user_id);
    if (online.error) return ;
    if (online.status == 0)
    {
        circle.classList.add("online-status-circle-offline");
        radar.classList.add("online-status-radar-offline");
    }
}