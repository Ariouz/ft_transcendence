async function addGameToLeaderboard(userData, userLang, fragment)
{

    let userPublicData = await retrievePublicProfileDataById(userData.user_id);
    if (userPublicData.error)
        return ;

    let userEntry = document.createElement("tr");
    userEntry.classList.add("leaderboard_row");
    
    let userInfoCell = document.createElement("td");
    userInfoCell.classList.add("leaderboard_user_info");
    
    let avatarContainer = document.createElement("div");
    avatarContainer.classList.add("pong_leaderboard_avatar");
    
    let avatarImg = document.createElement("img");
    avatarImg.src = userPublicData.avatar;
    avatarImg.width = 90;
    avatarImg.style.height = "auto";
    
    avatarContainer.appendChild(avatarImg);
    
    let usernameSpan = document.createElement("span");
    usernameSpan.textContent = userPublicData.username;
    
    userInfoCell.appendChild(avatarContainer);
    userInfoCell.appendChild(usernameSpan);
    
    let rankCell = document.createElement("td");
    rankCell.textContent = `#${userData.rank}`;
    
    let playedCell = document.createElement("td");
    playedCell.textContent = userData.played;
    
    let winsCell = document.createElement("td");
    winsCell.textContent = userData.wins;
    
    let winRateCell = document.createElement("td");
    winRateCell.textContent = `${Math.floor(userData.win_rate)}%`;
    
    userEntry.appendChild(userInfoCell);
    userEntry.appendChild(rankCell);
    userEntry.appendChild(playedCell);
    userEntry.appendChild(winsCell);
    userEntry.appendChild(winRateCell);

    fragment.appendChild(userEntry);
}

async function loadLeaderboard(page)
{
    let itemsPerPage = 6;
    
    let leaderboardData = await getLeaderboardData(page * itemsPerPage, itemsPerPage);
    let leaderboardList = document.getElementById("leaderboard_table_content");
    
    let userCount = leaderboardData.user_count;
    g_leaderboardMaxPage = userCount / itemsPerPage;
    
    let userLang = `${SELECTED_LANGUAGE}-${SELECTED_LANGUAGE.toUpperCase()}`;
    
    let leaderboard = leaderboardData.leaderboard;
    
    if (Object.values(leaderboard).length == 0)
    {
        leaderboardList.innerHTML = "";
        document.getElementById("leaderboard_error").style.display = "block";
        document.getElementById("leaderboard_error").innerText = await fetchTranslation("leaderboard_no_user");
        return ;
    }
    
    fragment = document.createDocumentFragment();
    for (user in leaderboard)
        await addGameToLeaderboard(leaderboard[user], userLang, fragment);

    leaderboardList.replaceChildren(fragment);
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