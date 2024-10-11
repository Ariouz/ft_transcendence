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