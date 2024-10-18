async function getGameData(game_id)
{
    let url = `${PONG_SERVICE_URL}/game/data/?game_id=${game_id}`;
    
    let gData = await fetch(url)
    .then(data => data.json())
    .then(data => {
        return data;
    })
    .catch(error => {
        return error;
    })
    return gData;
}

async function sendStartLocalGameRequest(game_id)
{
    let url = `${PONG_SERVICE_URL}/game/start/`;
    let requestData = { game_id: game_id };
    
    await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
    }).then(data => data.json())
    .then(data => {})
    .catch(error => {
        console.log(error);
    });
}

async function canJoinGame(game_id, user_id)
{
    let url = `${PONG_SERVICE_URL}/game/can-join/`;
    let requestData = { game_id: game_id, user_id: user_id };
    
    return await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
    }).then(data => data.json())
    .then(data => {return data})
    .catch(error => {
        console.log(error);
        return error;
    });
}