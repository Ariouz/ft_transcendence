function displayRulesPopup()
{
    blackScreen = document.getElementById("black_screen_filter");
    blackScreen.style.opacity = "0.5";
    blackScreen.classList.add("black_screen_filter");
    
    popup = document.getElementById("pong_home_rules_popup");
    popup.style.top = "45%";
    popup.style.opacity = "1";
    popup.style.display = "block";
    popup.classList.add("pong_home_rules_popup");
}

function closeRulesPopup()
{
    blackScreen = document.getElementById("black_screen_filter");
    blackScreen.style.opacity = "0";
    
    popup = document.getElementById("pong_home_rules_popup");
    popup.style.top = "40%";
    popup.style.opacity = "0%";
    setTimeout(() => {
        blackScreen.classList.remove("black_screen_filter");
        popup.style.display = "none";
        if (popup.style.opacity != "0%") return ;
        popup.classList.remove("pong_home_rules_popup");
    }, 500);
}

function joinMatchmakingQueue(gameType)
{
    navigate(`/pong/matchmaking?game_type=${gameType}`);
}

async function displayActiveGameCard()
{
    let userIdReq = await retrieveId(getCookieAcccessToken());
    if (userIdReq.error) return ;
    let userId = userIdReq.user_id;

    let gameData = await getActiveGameId(userId);
    if (!gameData || !gameData.game_id) return ;

    let gameId = gameData.game_id;
    let container = document.getElementById("pongHomeActiveGameCard");
    if (!container) return ;

    let card = createElement("div", {class: "pongHomeActiveGame"}, [
        createElement("span", {}, await fetchTranslation("game_started")),
        createElement("button", {onclick: `navigate("/pong/game?gid=${gameId}")`}, await fetchTranslation("join"))
    ]);
    container.appendChild(card);
}

displayActiveGameCard();