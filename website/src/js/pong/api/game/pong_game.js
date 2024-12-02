function getDisplayNameByPlayer(player, players, user_id)
{
    if (players[player].id == user_id)
        return g_pongSelfDisplayName;
    else return g_pongOpponentDisplayName;
}