async function displayStartNextRoundButton(tournamentId)
{
    let startButton = document.getElementById("tournamentRoundStartNext");
    let startContainer = document.getElementById("tournament_rounds_actions_container");
    let isHost = await isTournamentPlayerHost(tournamentId);
    let state = await getTournamentState(tournamentId);

    let show = isHost && state == "ongoing";

    startButton.style.display = show ? "block" : "none";
    startContainer.style.display = show ? "flex" : "none";

    if (state == "finished")
    {
        startContainer.appendChild(createElement("div", {class: "tournament_rounds_button custom_button custom_button_green_fill", onclick:"navigate('/tournament')"}, await fetchTranslation("back_to_tournaments")));
        startContainer.style.display = "flex";
    }
}


async function generateTournamentRoundList(tournamentId, clearContainer=false)
{
    let response = await getTournamentRounds(tournamentId);

    let rounds = response.rounds;
    
    let container = document.getElementById("tournamentRoundsContainer");
    if (clearContainer) container.replaceChildren();
    
    rounds.forEach(async roundData =>  {
        let roundElement = await createRound(roundData);
        container.appendChild(roundElement);
    });
    
}

async function createRound(roundData) {
    let element = document.createElement("div");
    element.classList.add("column");

    roundData.matches.forEach(async matchData => {
        let match = await createMatch(matchData, roundData.current_round, roundData.total_rounds);
        element.appendChild(match);
    });

    return element;
}

async function createMatch(matchData, currentRound, totalRounds) {
    let { match_id, player1, player2, score1, score2, winner } = matchData;

    let player1DisplayNameReq = await retrieveDisplayName(player1);
    let player1DisplayName = player1DisplayNameReq.display_name;

    let player2DisplayNameReq = await retrieveDisplayName(player2);
    let player2DisplayName = player2DisplayNameReq.display_name;

    let container = document.createElement("div");
    container.classList.add("match");
    container.id = `tournament-match-${match_id}`
    
    let winnerClass = "";
    if (winner !== null) {
        winnerClass = winner === player1 ? "winner-top" : "winner-bottom";
        container.classList.add(winnerClass);
    }

    createMatchEntry(true, player1, player1DisplayName, score1, container);
    if (player1 != player2)
        createMatchEntry(false, player2, player2DisplayName, score2, container);

    createMatchLines(container, currentRound, totalRounds);

    return container;
}

function createMatchEntry(isTop, playerId, name, score, parent)
{
    let container = document.createElement("div");
    container.classList.add("team");
    container.classList.add(`match-${isTop ? "top": "bottom"}`);

    container.innerHTML = `
        <span class="image"></span>
        <span class="seed"></span>
        <span class="name"></span>
        <span class="score"></span>
    `;

    container.querySelector('.seed').textContent = playerId;
    container.querySelector('.name').textContent = name;
    container.querySelector('.score').textContent = score;

    parent.appendChild(container);
}
    
function createMatchLines(parent, currentRound, totalRounds)
{
    let lines = document.createElement("div");
    lines.classList.add("match-lines");
    lines.innerHTML = `
        <div class="line one"></div>
        <div class="line two"></div>
    `;

    let linesAlt = document.createElement("div");
    linesAlt.classList.add("match-lines");
    linesAlt.classList.add("alt");
    linesAlt.innerHTML = `<div class="line one"></div>`;

    if (currentRound > 1 && totalRounds > 1){
        parent.appendChild(lines);
        parent.appendChild(linesAlt);
    }
}

async function updateTournamentMatch(matchData) {
    let { match_id, score1, score2, winner } = matchData;

    const matchElement = document.getElementById(`tournament-match-${match_id}`);

    if (!matchElement)
        return;

    const topScoreElement = matchElement.querySelector('.match-top .score');
    const bottomScoreElement = matchElement.querySelector('.match-bottom .score');

    if (topScoreElement)
        topScoreElement.textContent = score1;

    if (bottomScoreElement)
        bottomScoreElement.textContent = score2;


    matchElement.classList.remove('winner-top', 'winner-bottom');
    if (winner != -1) {
        const topPlayerElement = matchElement.querySelector('.match-top');
        const winnerClass = winner === topPlayerElement.querySelector('.seed').textContent ? 'winner-top' : 'winner-bottom';
        matchElement.classList.add(winnerClass);
    }
}

async function endTournament(tid, winner_id)
{
    let startButton = document.getElementById("tournamentRoundStartNext");
    let startContainer = document.getElementById("tournament_rounds_actions_container");

    let winnerDisplayNameReq = await retrieveDisplayName(winner_id);
    let winnerDisplayName = winnerDisplayNameReq.display_name;

    if (startButton) startButton.remove();
    startContainer.appendChild(createElement("div", {class: "tournament_rounds_button custom_button custom_button_green_fill", onclick:"navigate('/tournament')"}, await fetchTranslation("back_to_tournaments")));
    startContainer.style.display = "flex";

    setTimeout(async () => {
        showNotification(`${winnerDisplayName} ${await fetchTranslation("tournament_has_won")}`, 5);
        if (g_tournamentWebSocket)
            g_tournamentWebSocket.close();
        g_tournamentWebSocket = null;
    }, 8 * 1000);
}