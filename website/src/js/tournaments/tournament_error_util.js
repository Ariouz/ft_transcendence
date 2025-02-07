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
    {
        doc.style.visibility = show ? "visible" : "hidden";
        doc.style.opacity = show ? "1" : "0";
        doc.style.maxHeight = show ? "200px" : "0";
    }
}