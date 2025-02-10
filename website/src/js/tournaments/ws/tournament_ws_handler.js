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
    displayTournamentSuccess(userDisplayName + " has joined"); // TODO translate using g_tournamentTranslations[key]
    addTournamentParticipantToList(userId);
}

async function handleTournamentUserLeftWS(data)
{
    let userId = data.user_id;
    let displayNameReq = await retrieveDisplayName(userId);
    console.log(displayNameReq);
    let userDisplayName = displayNameReq.display_name;
    displayTournamentSuccess(userDisplayName + " has left"); // TODO translate using g_tournamentTranslations[key]
    removeTournamentParticipantListEntry(userId);
}

async function handleTournamentDeleteWs()
{
    displayTournamentSuccess("Tournament cancelled");// TODO translate using g_tournamentTranslations[key]
    if (g_tournamentWebSocket)
        g_tournamentWebSocket.close()
    g_tournamentWebSocket = null;
    navigate("/tournament");
}

async function handleTournamentRoundUpdate(data)
{
    console.log(data);
    await updateTournamentMatch(data);
}

async function handleTournamentRoundGenerated(tid)
{
    await generateTournamentRoundList(tid, true);
}

async function handleTournamentEnded(data)
{
    console.log("Tournament end");
    await endTournament(data.tournament_id, data.winner_id);
}