async function generateTournamentListCard(tournamentId)
{
    let element = document.createElement("div");
    element.innerHTML = `
        <h4>Tournament #${tournamentId}</h4>
        <button onclick="joinTournament(${tournamentId})">Join</button>
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
        listContainer.appendChild(await generateTournamentListCard(tournamentData.tournament_id));
    }
}

loadList();