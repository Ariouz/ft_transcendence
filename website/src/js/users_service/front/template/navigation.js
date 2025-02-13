async function handleNavLoginButton()
{
    let navLogin = document.getElementById("nav_login");
    let navUser = document.getElementById("nav_user");

    let loggedIn = isLoggedIn();
    navLogin.style.display = loggedIn ? 'none' : 'flex';
    navUser.style.display = loggedIn ? 'flex' : 'none';
}

handleNavLoginButton();