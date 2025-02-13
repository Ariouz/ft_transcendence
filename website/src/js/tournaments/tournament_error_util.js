async function displayTournamentError(title, details)
{
    await fetchTranslation(title).then(txt => getTournamentErrorTitle().innerText = txt);
    await fetchTranslation(details).then(txt => getTournamentErrorDetails().innerText = txt);
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