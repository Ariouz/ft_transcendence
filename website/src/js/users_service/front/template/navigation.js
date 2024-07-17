function handleNavLoginButton()
{
    navLogin = document.getElementById("nav_login");
    navUser = document.getElementById("nav_user");

    let loggedIn = isLoggedIn();
    navLogin.style.display = loggedIn ? 'none' : 'block';
    navUser.style.display = loggedIn ? 'block' : 'none';

    
}