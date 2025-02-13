var g_tournamentParticipantCount = 0;

async function generateTournamentParticipantListEntry(user_id)
{
    let displayNameReq = await retrieveDisplayName(user_id);
    let userDisplayName = displayNameReq.display_name;

    let element = document.createElement("tr");
    let userIdCell = document.createElement("td");
    let userDisplayNameCell = document.createElement("td");
   
    userIdCell.textContent = user_id;
    userDisplayNameCell.textContent = userDisplayName;
    
    element.setAttribute("tournament-participant", user_id);
    element.appendChild(userIdCell);
    element.appendChild(userDisplayNameCell);
    
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
            element.remove();
            break;
        }
    }
}

function isTournamentParticipantListEntrySet(user_id, table)
{
    for (let element of table.children) {
        if (!element.hasAttribute("tournament-participant")) continue;
        if (element.getAttribute("tournament-participant") == user_id)
            return true;
    }
    return false;
}

async function addTournamentParticipantToList(user_id)
{
    let table = document.getElementById("tournamentParticipantsList");

    let exists = isTournamentParticipantListEntrySet(user_id, table);
    if (!table || exists) return;
    let element = await generateTournamentParticipantListEntry(user_id);

    table.appendChild(element);
    g_tournamentParticipantCount++;
    updateTournamentParticipantCount();

}

async function reloadTournamentParticipantList(tournament_id)
{
    let table = document.getElementById("tournamentParticipantsList");
    // if (!table) return ;
    table.innerHTML = "";

    let displayName = await fetchTranslation("display_name");
    let element = document.createElement("tr");
    element.innerHTML = `<th>Id</th><th data-i18n="display_name">${displayName}</th>`;
    table.appendChild(element);
    await loadTournamentParticipantsList(tournament_id);
}

async function loadTournamentParticipantsList(tournament_id)
{
    // await clearTournamentParticipantList();
    g_tournamentParticipantCount = 0;
    let participants = await getTournamentParticipants(tournament_id);
    for (let participantId of participants)
        await addTournamentParticipantToList(participantId);
}

function updateTournamentParticipantCount()
{
    let count = document.getElementById("tournamentParticipantsCount");
    count.innerText = g_tournamentParticipantCount;
}

async function displayTournamentLobbyButtons(tournamentId)
{
    let isHost = await isTournamentPlayerHost(tournamentId);

    let leaveButton = document.getElementById("tournamentLeaveButton");
    let deleteButton = document.getElementById("tournamentDeleteButton");
    let launchButton = document.getElementById("tournamentLaunchButton");

    leaveButton.style.display = isHost ? "none" : "block";
    deleteButton.style.display = !isHost ? "none" : "block";
    launchButton.style.display = !isHost ? "none" : "block";
}