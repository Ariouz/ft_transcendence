async function addGameToLeaderboard(userData, userLang, fragment)
{

    let userPublicData = await retrievePublicProfileDataById(userData.user_id);

    let userEntry = document.createElement("tr");
    userEntry.innerHTML = `

    <tr class="leaderboard_row">
        <td class="leaderboard_user_info">
            <div class="pong_leaderboard_avatar"><img src="${userPublicData.avatar}" alt="" width="90px" height="auto"></div>
            <span>${userPublicData.username}</span>
        </td>
        <td>#${userData.rank}</td>
        <td>${userData.played}</td>
        <td>${userData.wins}</td>
        <td>${Math.floor(userData.win_rate)}%</td>
    </tr>

    `;
    
    fragment.appendChild(userEntry);
}

async function loadLeaderboard(page)
{
    let itemsPerPage = 6;
    
    let userHistoryData = await getLeaderboardData(page * itemsPerPage, itemsPerPage);
    let historyList = document.getElementById("leaderboard_table_content");
    
    let userCount = userHistoryData.user_count;
    g_leaderboardMaxPage = userCount / itemsPerPage;
    
    let userLang = `${SELECTED_LANGUAGE}-${SELECTED_LANGUAGE.toUpperCase()}`;
    
    let history = userHistoryData.leaderboard;
    
    if (Object.values(history).length == 0)
    {
        historyList.innerHTML = "";
        document.getElementById("leaderboard_error").style.display = "block";
        document.getElementById("leaderboard_error").innerText = "No user to show"; // TODO TRANSLATE
        return ;
    }
    
    fragment = document.createDocumentFragment();
    for (game in history)
        await addGameToLeaderboard(history[game], userLang, fragment);
    
    historyList.replaceChildren(fragment);
    document.getElementById("leaderboard_error").style.display = "none";
}

async function showLeaderboard(page)
{
    if (!page) page = 0;
    if (page <= 0) page = 0;
    if (page == g_leaderboardPage) return ;
    g_leaderboardPage = page;
    
    await loadLeaderboard(page);
    document.getElementById("leaderboard_current_page").innerText = parseInt(page) + 1;
}

g_leaderboardPage = -1;
g_leaderboardMaxPage = 0;
g_leaderboardTranslations = {};

async function initLeaderboard()
{
    let access_token = getCookie("session_token");
    let userIdData = await retrieveId(access_token);
    await showLeaderboard(0);
}

initLeaderboard();