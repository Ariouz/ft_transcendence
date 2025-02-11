async function handleTournamentWs(e, user_token) {
    try {
        const data = JSON.parse(e.data);
        g_error_tournament_ws = false;
        if (data.type)
        {
            console.log(data.type);
            if (data.type == "user_joined")
                await handleTournamentUserJoinedWS(data);
            else if (data.type == "user_left")
                await handleTournamentUserLeftWS(data);
            else if (data.type == "tournament_delete")
                await handleTournamentDeleteWs();
            else if (data.type == "tournament_round_update")
                await handleTournamentRoundUpdate(data.data);
            else if (data.type == "rounds_generated")
                await handleTournamentRoundGenerated(data.tournament_id);
            else if (data.type == "tournament_started")
                navigate(`/tournament/rounds?tid=${data.tournament_id}`);
            else if (data.type == "tournament_ended")
                await handleTournamentEnded(data);
        }
        else
        g_error_tournament_ws = true;
    } catch (error) {
        g_error_tournament_ws = true;
    }
}

async function handleTournamentUserJoinedWS(data)
{
    let userId = data.user_id;
    let displayNameReq = await retrieveDisplayName(userId);
    console.log(displayNameReq);
    let userDisplayName = displayNameReq.display_name;
    displayTournamentSuccess(`${userDisplayName} ${await fetchTranslation("has_joined")}`);
    addTournamentParticipantToList(userId);
}

async function handleTournamentUserLeftWS(data)
{
    let state = await getTournamentState(tournamentId);
    if (state == "finished") return ;

    let userId = data.user_id;
    let displayNameReq = await retrieveDisplayName(userId);
    console.log(displayNameReq);
    let userDisplayName = displayNameReq.display_name;
    displayTournamentSuccess(`${userDisplayName} ${await fetchTranslation("has_left")}`);
    removeTournamentParticipantListEntry(userId);
}

async function handleTournamentDeleteWs()
{
    displayTournamentSuccess(await fetchTranslation("tournament_cancelled"));
    if (g_tournamentWebSocket)
        g_tournamentWebSocket.close()
    g_tournamentWebSocket = null;
    navigate("/tournament");
}

async function handleTournamentRoundUpdate(data)
{
    await updateTournamentMatch(data);
}

async function handleTournamentRoundGenerated(tid)
{
    await generateTournamentRoundList(tid, true);
}

async function handleTournamentEnded(data)
{
    await endTournament(data.tournament_id, data.winner_id);
}