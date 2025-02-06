async function displayStartNextRoundButton(tournamentId)
{
    let startButton = document.getElementById("tournamentRoundStartNext");
    let isHost = await isTournamentPlayerHost(tournamentId);

    startButton.style.display = isHost ? "block" : "none";
}


async function generateTournamentRoundList(tournamentId)
{
    let response = await getTournamentRounds(tournamentId);

    console.log("resp: " + response);
    let rounds = response.rounds;
    
    let container = document.getElementById("tournamentRoundsContainer");
    
    console.log("rounds: " + rounds);

    rounds.forEach(roundData => {
        let roundElement = createRound(roundData);
        container.appendChild(roundElement);
    });
    
}

function createRound(roundData) {
    let element = document.createElement("div");
    element.classList.add("column");

    roundData.matches.forEach(matchData => {
        let match = createMatch(matchData, roundData.current_round, roundData.total_rounds);
        element.appendChild(match);
    });

    return element;
}

function createMatch(matchData, currentRound, totalRounds) {
    let { match_id, player1, player2, score1, score2, winner } = matchData;

    let container = document.createElement("div");
    container.classList.add("match");
    
    let winnerClass = "";
    if (winner !== null) {
        winnerClass = winner === player1 ? "winner-top" : "winner-bottom";
        container.classList.add(winnerClass);
    }

    createMatchEntry(true, player1, `Joueur ${player1}`, score1, container);
    if (player1 != player2)
        createMatchEntry(false, player2, `Joueur ${player2}`, score2, container);

    createMatchLines(container, currentRound, totalRounds);

    return container;
}

function createMatchEntry(isTop, playerId, name, score, parent)
{
    let container = document.createElement("div");
    container.classList.add("team");
    container.classList.add(`match-${isTop ? "top": "bottom"}`);

    // replace by XSS protection for name
    container.innerHTML = `
        <span class="image"></span>
        <span class="seed">${playerId}</span>
        <span class="name">${name}</span>
        <span class="score">${score}</span>
    `;
    
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