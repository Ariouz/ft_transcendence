function handleRouting() {
    const path = window.location.pathname;
    const parts = path.split("/").filter(part => part !== "");
    const params = new URLSearchParams(window.location.search);
    setCookieBannerVisibility("none", "0"); 
    if (!doConsentCookies())
        setCookieBannerVisibility("flex", "100");

    if (g_userInPongQueue)
        leaveMatchmakingQueue().then(res => {}).catch(error => {});

    // close game ws to pause if the player leaves the page
    if (g_pongGameWebSocket)
    {
        g_pongGameWebSocket.close();
        g_pongGameType = null;
        g_pongGameState = null;
        g_pongGamePlayerPaddle = null;
        g_pongGameType = null;
        g_pongGameOpponentDisconnected = false;
        g_pongGameInterval = null;
    }

    Game.stopGameLoop();
    if (parts[0] === "api")
    {
        if (parts[1] === "auth")
            routeAuth(parts, params);
    }
    else if (parts[0] === "users")
    {
        routeUser(parts, params);
    }
    else if (parts[0] == "pong") {
        routePong(parts, params);
    }
    else if (path === "/cookie-policy")
    {
        loadContent("/pages/misc/cookie_policy.html");
    }
    else if (path === "/privacy-policy")
    {
        loadContent("/pages/misc/privacy_policy.html");
    }
    else if (path === '/login') {
        loadContent("/pages/user/auth/login.html");
    }
    else if (path === '/profile') {
        if (!isLoggedIn()) navigate("/login?redirect=profile");
        else loadContent("/pages/user/profile.html");
    }
    else if (parts[0] === 'settings') {
        if (!isLoggedIn()) navigate("/login?redirect=settings");
        else loadContent("/pages/user/settings.html");
    }
    else if (path === '/') {
        loadContent("/pages/home.html");
    }
    else if (parts[0] == "tournament"){
        routeTournament(parts, params);
    }
    else {
        if (path === "/user-error")
            loadContent("/pages/error/404user.html");
        else loadContent("/pages/error/404.html");
    }
}

function routeAuth(parts, params)
{
    if (parts.length < 4)
    {
        navigate("/error");
        return ;
    }

    if (parts[2] === "42")
    {
        if (parts[3] === "access")
        {
            let code = params.get("code");
            if (code === undefined) { navigate('/error'); return; }
            loadContent("/pages/user/auth/access_code.html");
            ftRetrieveClientAccessToken(code)
            .then(data => {
                token_data = JSON.parse(JSON.stringify(data));
                if (token_data.error) {
                    showUnavailableError();
                    console.log(token_data.error + " " + token_data.details);
                    navigate("/login");
                    return ;
                }
                data = retrieveFtData(token_data.access_token).then(data => {
                    createAccount(data.login, data.email, token_data.access_token, data.image.link, data.usual_full_name)
                        .then( r => {
                            setUserLanguage();
                        })
                }).catch(error => {
                    console.log(error);
                });
            }).catch(error => {
                console.log(error);
            });
        }
    }
}

function routeUser(parts, params)
{
    if (parts.length === 1)
    {
        if (!isLoggedIn())
            navigate("/login?redirect=users");
        else loadContent("/pages/users/list_users.html");
        return ;
    }

    if (parts.length !== 3)
    {
        navigate("/error");
        return ;
    }

    if (parts[1] === "profile")
        if (!isLoggedIn())
            navigate("/login?redirect=users/profile/"+parts[2]);
        else loadContent("/pages/users/public_profile.html");
}

function routePong(parts, params)
{
    const pages = {
        "matchmaking": "/pages/pong/pong_matchmaking.html",
        "history": "/pages/pong/pong_history.html",
        "leaderboard": "/pages/pong/pong_leaderboard.html"
    };

    if (parts.length === 1)
    {
        loadContent("/pages/pong/pong_home.html");
    }
    else if (parts[1] === "game")
    {
        loadContent("/pages/pong/pong_game.html");
    }
    else if (pages[parts[1]]) {
        if (!isLoggedIn())
            navigate(`/login?redirect=pong/${parts[1]}`);
        else
            loadContent(pages[parts[1]]);
    }
    else
        loadContent("/pages/error/404.html");

}

function routeTournament(parts, params)
{
    const pages = {
        "lobby": "/pages/tournaments/tournament_lobby.html",
        "rounds": "/pages/tournaments/tournament_rounds.html",
        "recap": "/pages/tournaments/tournament_ending.html"
    };

    if (!isLoggedIn())
        navigate("/login?redirect=tournament");

    else if (parts.length === 1)
    {
        loadContent("/pages/tournaments/tournament_home.html");
    }
    else if (pages[parts[1]]) {
        loadContent(pages[parts[1]]);
    }
    else
        loadContent("/pages/error/404.html");

}

function loadContent(url, onPageLoaded = () => {}) {
    fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(html => {
        showNavigationAndFooter();
        document.getElementById('page_content').innerHTML = "";
        handleNavLoginButton();
        document.getElementById('page_content').innerHTML = html;
        return executeScripts(document.getElementById('page_content'));
    })
    .then(() => {
        updateI18nOnNewPage();
        onPageLoaded();
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

function executeScripts(element) {
    const scripts = element.querySelectorAll('script');
    const promises = [];

    scripts.forEach(script => {
        const newScript = document.createElement('script');
        if (script.src) {
            newScript.src = script.src;
            const promise = new Promise((resolve, reject) => {
                newScript.onload = resolve;
                newScript.onerror = reject;
            });
            promises.push(promise);
        } else {
            newScript.textContent = script.textContent;
        }
        document.body.appendChild(newScript);
        document.body.removeChild(newScript);
    });
    return Promise.all(promises);
}

handleRouting();

window.addEventListener('popstate', handleRouting);

function navigate(path) {
    history.pushState(null, null, path);
    handleRouting();
}
