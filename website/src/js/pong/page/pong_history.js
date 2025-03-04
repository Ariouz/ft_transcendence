function isWinner(userId, game)
{
    return game.winner_id == userId;
}

function translateGameDate(gameDate, userLang)
{
    const date = new Date(gameDate);
    
    const formattedDate = new Intl.DateTimeFormat(userLang, {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    }).format(date);
    return formattedDate;
}

async function addGameToHistory(game, userId, userLang, fragment) {
    let opponentId = game.users[0] == userId ? game.users[1] : game.users[0];
    let opponentData = await retrievePublicProfileDataById(opponentId);

    let gameEntry = createElement("li", {
        class: `history_item history_${isWinner(userId, game) ? "win" : "defeat"}`
    });

    let userInfoDiv = createElement("div", { class: "history_user_info" }, [
        createElement("div", { class: "pong_history_avatar" }, [
            createElement("img", {
                src: opponentData.avatar == undefined ? "../../assets/images/default_avatar.svg" : opponentData.avatar,
                alt: "Opponent Avatar",
                width: "90px",
                height: "auto"
            })
        ]),
        createElement("span", {}, opponentData.display_name == undefined ? "<Deleted user>" : opponentData.display_name)
    ]);

    let scoreDiv = createElement("div", { class: "history_score" }, [
        createElement("div", { class: "history_score_win_status" }, 
            g_historyTranslations[isWinner(userId, game) ? 'victory' : 'defeat']
        ),
        createElement("div", { class: "history_score_score" }, 
            `${isWinner(userId, game) ? Math.max(game.score[0], game.score[1]) : Math.min(game.score[0], game.score[1])}
                         - 
            ${isWinner(userId, game) ? Math.min(game.score[0], game.score[1]) : Math.max(game.score[0], game.score[1])}`
        )
    ]);

    let gameInfoDiv = createElement("div", { class: "history_game_info" }, [
        createElement("div", {}, g_historyTranslations[game.type]),
        createElement("div", {}, translateGameDate(game.date, userLang))
    ]);

    [userInfoDiv, scoreDiv, gameInfoDiv].forEach(el => gameEntry.appendChild(el));
    fragment.appendChild(gameEntry);
}

async function loadHistory(page)
{
    let userId = g_historyUserId;
    let itemsPerPage = 6;
    
    let userHistoryData = await getUserGameHistory(userId, page * itemsPerPage, itemsPerPage);
    
    let historyList = document.getElementById("history_list");
    
    let onlineGamesPlayed = userHistoryData.online_games_played;
    g_historyMaxPage = onlineGamesPlayed / itemsPerPage;
    
    if (userHistoryData.error)
    {
        historyList.innerHTML = "";
        document.getElementById("history_error").style.display = "block";
        document.getElementById("history_error").innerText = g_historyTranslations['pong_history_no_game'];
        return ;
    }
    
    let userLang = `${SELECTED_LANGUAGE}-${SELECTED_LANGUAGE.toUpperCase()}`;
    
    let history = userHistoryData.history;
    if (!history)
        return ;
    
    if (Object.values(history).length == 0)
    {
        historyList.innerHTML = "";
        document.getElementById("history_error").style.display = "block";
        document.getElementById("history_error").innerText = g_historyTranslations['pong_history_no_game'];
        return ;
    }
    
    history = Object.values(history).reverse();
    fragment = document.createDocumentFragment();
    
    for (game in history)
        await addGameToHistory(history[game], userId, userLang, fragment);
    
    historyList.replaceChildren(fragment);
    document.getElementById("history_error").style.display = "none";
}

async function showHistory(page)
{
    if (!page) page = 0;
    if (page <= 0) page = 0;
    if (page == g_historyPage) return ;
    g_historyPage = page;
    
    await loadHistory(page);
    document.getElementById("history_current_page").innerText = parseInt(page) + 1;
}

async function loadTranslations()
{
    g_historyTranslations['pong_history_no_game'] = await fetchTranslation("pong_history_no_game");
    g_historyTranslations['pong_history_no_user'] = await fetchTranslation("user_not_found");
    g_historyTranslations['victory'] = await fetchTranslation("victory");
    g_historyTranslations['defeat'] = await fetchTranslation("defeat");
    g_historyTranslations['1v1'] = await fetchTranslation("pong_type_1v1");
    g_historyTranslations['arcade'] = await fetchTranslation("pong_type_arcade");
    g_historyTranslations['tournament'] = await fetchTranslation("pong_type_tournament");
}

g_historyPage = -1;
g_historyMaxPage = 0;
g_historyTranslations = {};
g_historyUserId = 0;

async function initHistory()
{

    path = window.location.pathname;
    parts = path.split("/");
    parts.shift();

    let userIdData;

    if (parts.length != 3) 
    {
        let sessionToken = getCookie("session_token");
        userIdData = await retrieveId(sessionToken);
    }else
    {
        let targetUsername = parts[2];
        userIdData = await retrievePublicProfileDataByUsername(targetUsername);
    }
    
    if (!userIdData) return ;
    if (userIdData.error)
    {
        navigate("/user-error");
        return ;
    }

    g_historyUserId = userIdData.user_id;
    await loadTranslations();
    await showHistory(0);
}

initHistory();