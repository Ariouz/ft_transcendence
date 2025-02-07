async function generateTournamentListCard(tournamentId, playerCount)
{
    let element = document.createElement("div");
    element.classList.add("tournamentListItem");
    element.innerHTML = `
        <div class="tournamentListItemTopSection">
            <span class="tournamentListItemTitle"><span data-i18n="tournament"></span> #${tournamentId}</span>
            <span class="tournamentListItemPlayerCount">${playerCount} players</span>
        </div>
        <div>
            <button class="tournamentListItemJoinButton" onclick="joinTournament(${tournamentId})">Join</button>
        </div>
        `;
    return element;
}

async function loadList()
{
    let listContainer = document.getElementById("tournaments_list");
    
    let list = await getTournaments();
    console.log(list);
    for (tournament in list)
    {
        let tournamentData = list[tournament];
        listContainer.appendChild(await generateTournamentListCard(tournamentData.tournament_id, tournamentData.player_count));
    }
}

loadList();