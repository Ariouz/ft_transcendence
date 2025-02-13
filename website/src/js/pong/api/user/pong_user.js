async function getPongUserStats(user_id)
{
    let url = `${PONG_SERVICE_URL}/user/stats/${user_id}`;
    
    return await fetch(url)
    .then(data => data.json())
    .then(data => {return data})
    .catch(async error => {
        await showUnavailableError();
        return error;
    });
}

async function getUserGameHistory(user_id, offset, limit)
{
    let url = `${PONG_SERVICE_URL}/user/game-history/${user_id}?offset=${offset}&limit=${limit}`;
    
    return await fetch(url)
    .then(data => data.json())
    .then(data => {return data})
    .catch(async error => {
        await showUnavailableError();
        return error;
    });
}