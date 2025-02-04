async function generateTournamentRoundList(tournamentId)
{
    let rounds = await getTournamentRounds(tournamentId).rounds;
    
    let container = document.getElementById("tournamentRoundsContainer");
    
    // test
    let round = createRound(1);
    console.log(container);
    container.appendChild(round);

    let round2 = createRound(2);
    console.log(container);
    container.appendChild(round2);
    
    console.log(rounds);
}

function createRound(roundId)
{
    let element = document.createElement("div");
    element.classList.add("column");
    
    let p1 = {name: "Player 1", id: 0, score: 3};
    let p2 = {name: "Player 2", id: 1, score: 1};
    let p3 = {name: "Player 3", id: 2, score: 2};
    let p4 = {name: "Player 4", id: 3, score: 5};

    let match = createMatch(0, p1, p2);
    element.appendChild(match);

    if (roundId == 1)
    {
        let match2 = createMatch(0, p3, p4);
        element.appendChild(match2);
    }

    return element;
}

function createMatch(matchId, p1, p2)
{
    let container = document.createElement("div");
    container.classList.add("match");
    container.classList.add(`winner-${p1.score > p2.score ? "top" : "bottom"}`);
    
    createMatchEntry(true, p1.id, p1.name, p1.score, container);
    createMatchEntry(false, p2.id, p2.name, p2.score, container);
    
    createMatchLines(container);
    
    return container;
}

function createMatchEntry(isTop, playerId, name, score, parent)
{
    let container = document.createElement("div");
    container.classList.add("team");
    container.classList.add(`match-${isTop ? "top": "bottom"}`);
    container.innerHTML = `
        <span class="image"></span>
        <span class="seed">${playerId}</span>
        <span class="name">${name}</span>
        <span class="score">${score}</span>
    `;
    
    parent.appendChild(container);
}
    
function createMatchLines(parent)
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

    parent.appendChild(lines);
    parent.appendChild(linesAlt);
}