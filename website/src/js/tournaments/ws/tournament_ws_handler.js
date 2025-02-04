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

