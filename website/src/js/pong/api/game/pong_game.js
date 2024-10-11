// check if game state is init or started, player has the right to join
async function checkGame(user_id, game_id)
{
    let gameData = await getGameData(game_id);
    if (gameData.error)
    {
        console.error(gameData);
        return ;
    }

    console.log(gameData);
}