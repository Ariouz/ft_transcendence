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
    else if (path === '/pong') {
        loadContent("/pages/pong.html");
    }
    else if (path === '/') {
        loadContent("/pages/home.html");
    }
    else {
        loadContent("/pages/error/404.html");
    }
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
            console.log(code);

            ftRetrieveClientAccessToken(code)
            .then(data => {
                token_data = JSON.parse(JSON.stringify(data));
                console.log("Access token: " + token_data.access_token);
                setCookie("session_token", token_data.access_token, 0, token_data.expires_in);
                navigate("/");
            }).catch(error => {
                console.error(error);
            });
        }
    }
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
