async function getLeaderboardData(offset, limit)
{
    let url = `${PONG_SERVICE_URL}/all/leaderboard/?offset=${offset}&limit=${limit}`;
    
    return await fetch(url)
    .then(data => data.json())
    .then(data => {return data})
    .catch(error => {
        console.log(error);
        return error;
    });
}