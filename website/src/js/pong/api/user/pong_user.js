async function getPongUserStats(user_id)
{
    let url = `${PONG_SERVICE_URL}/user/stats/${user_id}`;
    
    return await fetch(url)
    .then(data => data.json())
    .then(data => {return data})
    .catch(error => {
        console.log(error);
        return error;
    });
}