let g_tournamentParticipantCount = 0;

async function generateTournamentParticipantListEntry(user_id)
{
    let displayNameReq = await retrieveDisplayName(user_id);
    let userDisplayName = displayNameReq.display_name;

    let element = document.createElement("tr");
    element.innerHTML = `
        <td>${user_id}</td>
        <td>${userDisplayName}</td>
    `;
    element.setAttribute("tournament-participant", user_id);
    return element;
}

function removeTournamentParticipantListEntry(user_id)
{
    let table = document.getElementById("tournamentParticipantsList");
    for (let element of table.children) {
        if (element.getAttribute("tournament-participant") == user_id)
        {
            g_tournamentParticipantCount--;
            updateTournamentParticipantCount();
            table.removeChild(element);
            break;
        }
    }
}

function isTournamentParticipantListEntrySet(user_id, table)
{
    for (let element of table.children) {
        if (element.getAttribute("tournament-participant") == user_id)
            return true;
    }
    return false;
}

async function addTournamentParticipantToList(user_id)
{
    let table = document.getElementById("tournamentParticipantsList");

    if (isTournamentParticipantListEntrySet(user_id, table)) return;
    let element = await generateTournamentParticipantListEntry(user_id);

    table.appendChild(element);
    g_tournamentParticipantCount++;
    updateTournamentParticipantCount();

}

async function loadTournamentParticipantsList(tournament_id)
{
    let participants = await getTournamentParticipants(tournament_id);
    for (let participantId of participants)
        await addTournamentParticipantToList(participantId);
}

function updateTournamentParticipantCount()
{
    let count = document.getElementById("tournamentParticipantsCount");
    count.innerText = g_tournamentParticipantCount;
}