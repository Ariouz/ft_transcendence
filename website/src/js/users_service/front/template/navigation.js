async function handleNavLoginButton()
{
    navLogin = document.getElementById("nav_login");
    navUser = document.getElementById("nav_user");

    let loggedIn = isLoggedIn();
    navLogin.style.display = loggedIn ? 'none' : 'flex';
    navUser.style.display = loggedIn ? 'flex' : 'none';

    if (loggedIn)
    {
        let access_token = getCookieAcccessToken();
        let username = await retrieveUsername(access_token)
        .then(data => {
            return data.username;
        })
        .catch(error => {console.error(error); return "Error"});
        navUser.innerText = username;
    }
}

handleNavLoginButton();