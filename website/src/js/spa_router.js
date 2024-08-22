function handleRouting() {
    const path = window.location.pathname;
    const parts = path.split("/");
    const params = new URLSearchParams(window.location.search);

    parts.shift();
    console.log(parts);
    if (parts[0] == "api")
    {
        if (parts[1] == "auth")
            routeAuth(parts, params);
    }
    else if (parts[0] == "users")
    {
        routeUser(parts, params);
    }
    else if (path === '/pong') {
        loadContent("/pages/pong.html");
    }
    else if (path === '/login') {
        loadContent("/pages/user/auth/login.html");
    }
    else if (path === '/profile') {
        if (!isLoggedIn()) navigate("/login");
        else loadContent("/pages/user/profile.html");
    }
    else if (parts[0] === 'settings') {
        if (!isLoggedIn()) navigate("/login");
        else loadContent("/pages/user/settings.html");
    }
    else if (path === '/') {
        loadContent("/pages/home.html");
    }
    else {
        loadContent("/pages/error/404.html");
    }
    updateContentOnNewPage();
}

function routeAuth(parts, params)
{
    if (parts.length < 4)
    {
        navigate("/error");
        return ;
    }

    if (parts[2] == "42")
    {
        if (parts[3] == "access")
        {
            code = params.get("code");
            if (code == undefined) { navigate('/error'); return; }
            console.log(code);
            loadContent("/pages/user/auth/access_code.html");
            ftRetrieveClientAccessToken(code)
            .then(data => {
                token_data = JSON.parse(JSON.stringify(data));
                console.log(token_data);
                if (token_data.error) {
                    alert("An error occured, please try again.");
                    navigate("/login");
                    return ;
                }
                console.log("Access token: " + token_data.access_token);
                data = retrieveFtData(token_data.access_token).then(data => {
                    console.log(data);
                    createAccount(data.login, data.email, token_data.access_token, data.image.link, data.usual_full_name);
                }).catch(error => {
                    console.error(error);
                });
            }).catch(error => {
                console.error(error);
            });
        }
    }
}

function routeUser(parts, params)
{
    if (parts.length == 1)
    {
        if (!isLoggedIn())
            navigate("/login");
        else loadContent("/pages/users/list_users.html");
        return ;
    }

    if (parts.length != 3)
    {
        navigate("/error");
        return ;
    }

    if (parts[1] == "profile")
        if (!isLoggedIn())
            navigate("/login");
        else loadContent("/pages/users/public_profile.html");
}

function loadContent(url) {
    fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(html => {
        document.getElementById('page_content').innerHTML = "";
        handleNavLoginButton();
        document.getElementById('page_content').innerHTML = html;
        executeScripts(document.getElementById('page_content'));
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

function executeScripts(element) {
    const scripts = element.querySelectorAll('script');
    scripts.forEach(script => {
        const newScript = document.createElement('script');
        if (script.src) {
            newScript.src = script.src;
        } else {
            newScript.textContent = script.textContent;
        }
        document.body.appendChild(newScript);
        document.body.removeChild(newScript);
    });
}

handleRouting();

window.addEventListener('popstate', handleRouting);

function navigate(path) {
    history.pushState(null, null, path);
    handleRouting();
}
