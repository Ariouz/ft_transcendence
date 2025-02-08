async function generateTournamentListCard(tournamentId, playerCount)
{
    let element = document.createElement("div");
    element.classList.add("tournamentListItem");
    element.innerHTML = `
        <div class="tournamentListItemTopSection">
            <span class="tournamentListItemTitle"><span data-i18n="tournament"></span> #${tournamentId}</span>
            <span class="tournamentListItemPlayerCount"><span data-i18n='players'></span>: ${playerCount}</span>
        </div>
        <div>
            <button class="tournamentListItemJoinButton" onclick="joinTournament(${tournamentId})" data-i18n='join'></button>
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

async function loadHostedTournamentCard()
{
    let tournamentData = await getHostedTournament();
    if (tournamentData.tournament_id == -1) return ;

    let createContainer = document.getElementById("tournamentHostCreateContainer")
    if (createContainer) createContainer.remove();

    let container = document.getElementById("tournamentHomeListHostSection");
    if (!container) return ;

    let element = createElement("div", {class: "tournamentListItem", id: "tournamentHostedContainer"},
        [
            createElement("div", {class: "tournamentListItemTopSection"}, [
                createElement("span", {class: "tournamentListItemTitle"}, `${await fetchTranslation("your_tournament")} (#${tournamentData.tournament_id})`),
                createElement("span", {class: "tournamentListItemPlayerCount"}, [
                    createElement("span", {}, await fetchTranslation("players")),
                    createElement("span", {}, `: ${tournamentData.participant_count}`)
                ]),
            ]),
            createElement("div", {}, [
                createElement("button", {class: "tournamentListItemJoinButton", onclick: `navigate('/tournament/lobby/?tid=${tournamentData.tournament_id}')`}, await fetchTranslation("go_to_lobby"))
            ])
        ]
    );
    container.appendChild(element);
    console.log("append");
}

loadList();
loadHostedTournamentCard();