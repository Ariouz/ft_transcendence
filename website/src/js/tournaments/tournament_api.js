const TOURNAMENT_URL = `${PONG_SERVICE_URL}/tournament`;


async function createTournament() {
    let url = `${TOURNAMENT_URL}/create/`;

    let userIdReq = await retrieveId(getCookieAcccessToken());
    if (userIdReq.error) return ;
    let userId = userIdReq.user_id;

    let requestData = { host_id: userId };
    postWithCsrfToken(url, requestData, true)
    .then(data => {
        let tournamentId = data.tournament_id;
        displayTournamentSuccess(data.success);
        console.log(`Created tournament ${tournamentId}`);
        // navigate(`/tournament/lobby?tid=${tournamentId}`);
    })
    .catch(error => {
        displayTournamentError(error.error, error.details);
    });
}

async function doesPlayerParticipate(tournamentId)
{
    let url = `${TOURNAMENT_URL}/does-participates/`;

    let userIdReq = await retrieveId(getCookieAcccessToken());
    if (userIdReq.error) return ;
    let userId = userIdReq.user_id;

    let requestData = { user_id: userId, tournament_id: tournamentId };
    let retVal = postWithCsrfToken(url, requestData, true)
    .then(data => {
       return data.participates;
    })
    .catch(error => {
        return false;
    });

    return retVal;
}

async function isTournamentPlayerHost(tournamentId)
{
    let url = `${TOURNAMENT_URL}/is-host/`;

    let userIdReq = await retrieveId(getCookieAcccessToken());
    if (userIdReq.error) return ;
    let userId = userIdReq.user_id;

    let requestData = { user_id: userId, tournament_id: tournamentId };
    let retVal = postWithCsrfToken(url, requestData, true)
    .then(data => {
       return data.is_host;
    })
    .catch(error => {
        return false;
    });

    return retVal;
}

async function getTournamentState(tournamentId)
{
    let url = `${TOURNAMENT_URL}/state/`;

    let requestData = { tournament_id: tournamentId };
    let retVal = postWithCsrfToken(url, requestData, true)
    .then(data => {
       return data.state;
    })
    .catch(error => {
        return "finished";
    });

    return retVal;
}

async function deleteTournament(tournamentId)
{
    let url = `${TOURNAMENT_URL}/delete/`;

    let userIdReq = await retrieveId(getCookieAcccessToken());
    if (userIdReq.error) return ;
    let userId = userIdReq.user_id;

    let requestData = { user_id: userId, tournament_id: tournamentId };
    postWithCsrfToken(url, requestData, true)
    .then(data => {
       displayTournamentSuccess(data.success);
       console.log(data);
       if (g_tournamentWebSocket) g_tournamentWebSocket.close();
        g_tournamentWebSocket = null;
       navigate("/tournament");
    })
    .catch(error => {
        displayTournamentError(error.error, error.details);
    });

}

async function joinTournament(tournamentId)
{
    let url = `${TOURNAMENT_URL}/join/`;

    let userIdReq = await retrieveId(getCookieAcccessToken());
    if (userIdReq.error) return ;
    let userId = userIdReq.user_id;

    let requestData = { user_id: userId, tournament_id: tournamentId };
    postWithCsrfToken(url, requestData, true)
    .then(data => {
       displayTournamentSuccess(data.success);
       console.log(data);
    //    navigate(`/tournament/lobby?tid=${data.tournament_id}`);
    })
    .catch(error => {
        displayTournamentError(error.error, error.details);
    });
}

async function leaveTournament(tournamentId)
{
    let url = `${TOURNAMENT_URL}/leave/`;

    let userIdReq = await retrieveId(getCookieAcccessToken());
    if (userIdReq.error) return ;
    let userId = userIdReq.user_id;

    let requestData = { user_id: userId, tournament_id: tournamentId };
    postWithCsrfToken(url, requestData, true)
    .then(data => {
       displayTournamentSuccess(data.success);
       console.log(data);
       if (g_tournamentWebSocket) g_tournamentWebSocket.close();
       g_tournamentWebSocket = null;
       navigate(`/tournament`);
    })
    .catch(error => {
        displayTournamentError(error.error, error.details);
    });
}

async function getTournaments()
{
    let url = `${TOURNAMENT_URL}/list/`;

    let data = postWithCsrfToken(url, {}, true)
    .then(data => {
        console.log(data.data);
        return data.data;
    })
    .catch(error => {
        console.error(error);
        return {};
    });
    return data;
}

async function getTournamentParticipants(tournamentId)
{
    let url = `${TOURNAMENT_URL}/participants/`;

    let data = postWithCsrfToken(url, {tournament_id: tournamentId}, true)
    .then(data => {
        return data.participants;
    })
    .catch(error => {
        console.error(error);
        return [];
    });
    return data;
}

async function askToConnectToTournamentWS(tournamentId)
{
    let url = `${TOURNAMENT_URL}/ws-connect/`;

    let userIdReq = await retrieveId(getCookieAcccessToken());
    if (userIdReq.error) return ;
    let userId = userIdReq.user_id;

    let requestData = { user_id: userId, tournament_id: tournamentId };
    postWithCsrfToken(url, requestData, true)
    .then(data => {
    //    navigate(`/tournament/lobby?tid=${data.tournament_id}`);
    })
    .catch(error => {
        if (g_tournamentWebSocket) g_tournamentWebSocket.close();
        g_tournamentWebSocket = null;
        navigate("/tournament")
        displayTournamentError(error.error, error.details);
    });
}

async function launchTournament(tournamentId)
{
    let url = `${TOURNAMENT_URL}/launch/`;

    let userIdReq = await retrieveId(getCookieAcccessToken());
    if (userIdReq.error) return ;
    let userId = userIdReq.user_id;

    let requestData = { user_id: userId, tournament_id: tournamentId };
    postWithCsrfToken(url, requestData, true)
    .then(data => {
       console.log(data);
       navigate(`/tournament/rounds?tid=${tournamentId}`);
    })
    .catch(error => {
        displayTournamentError(error.error, error.details);
    });
}


async function getTournamentRounds(tournamentId)
{
    let url = `${TOURNAMENT_URL}/get-rounds/`;

    let requestData = { tournament_id: tournamentId };
    return postWithCsrfToken(url, requestData, true)
    .then(data => {
       console.log(data);
       return data;
    })
    .catch(error => {
        displayTournamentError(error.error, error.details);
        return {rounds: []};
    });
}