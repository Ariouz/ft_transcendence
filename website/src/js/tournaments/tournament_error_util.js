function displayTournamentError(title, details)
{
    getTournamentErrorTitle().innerText = title;
    getTournamentErrorDetails().innerText = details;
    setTournamentErrorDivDisplay(true);
}

async function displayTournamentSuccess(message)
{
    showNotification(`${message}`, 3);
    setTournamentErrorDivDisplay(false);
}

function getTournamentErrorTitle()
{
    return document.getElementById("tournamentErrorTitle");
}

function getTournamentErrorDetails()
{
    return document.getElementById("tournamentErrorDetails");
}

function setTournamentErrorDivDisplay(show)
{
    let doc = document.getElementById("tournamentErrorDiv");
    if (doc)
        doc.style.display = show ? "block" : "none";
}