async function handleNavLoginButton()
{
    navLogin = document.getElementById("nav_login");
    navUser = document.getElementById("nav_user");

    let loggedIn = isLoggedIn();
    navLogin.style.display = loggedIn ? 'none' : 'flex';
    navUser.style.display = loggedIn ? 'flex' : 'none';
}

handleNavLoginButton();