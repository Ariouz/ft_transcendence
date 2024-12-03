function setCookie(name, value, days=7, seconds=null) {
    let expires = "";
    let date = new Date();
    if (seconds) {
        date.setTime(date.getTime() + (seconds * 1000));
    } else if (days) {
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    }
    expires = "; expires=" + date.toUTCString();
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    let nameEQ = name + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function deleteCookie(name)
{
    document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

function isLoggedIn()
{
    let session_token = getCookie("session_token");
    return session_token != null;
}

function logout()
{
    if (g_pongUserWebSocket) g_pongUserWebSocket.close();
    if (g_pongGameWebSocket) g_pongWebSocket.close();
    if (g_friendListWebSocket) g_friendListWebSocket.close();
    
    deleteCookie("session_token");
    updateLanguagePreferenceRemoval()
        .then( _ => {
        navigate('/');
    });
}

function revokeAllCookies()
{
    logout();
    deleteCookie("redirect");
    deleteCookie("cookie_consent");
    window.location.reload();
}

async function fetchBack(url)
{
    try {
        const response = await fetch(url);
        const data = await response.json();

        if (response.ok) {
            return data;
        } else {
            return data;
        }
    } catch (error) {
        console.log("Failed to fetch:" + error);
    }
}

function showNotification(text, duration)
{
    const animatedDiv = document.getElementById('notification_div');

    animatedDiv.classList.add('show');
    animatedDiv.innerText = text;

    setTimeout(() => {
        animatedDiv.classList.remove('show');
    }, duration * 1000);
}

function setRedirectCookie(redirect)
{
    if (doConsentCookies())
        setCookie("redirect", redirect);
}

function navigateToRedirectOr(defaultURL)
{
    let redirectCookie = getCookie("redirect");
    if (redirectCookie)
    {
        navigate("/" + redirectCookie);
        deleteCookie("redirect");
    }
    else
        navigate(defaultURL);
}

function doConsentCookies()
{
    return getCookie("cookie_consent");
}

function toggleDisplay(selector, show) {
    document.querySelector(selector).style.display = show ? '' : 'none';
}

function showMainNavigation()
{
    toggleDisplay('.main_nav', true);
}

function showFooter()
{
    toggleDisplay('footer', true);
}

function hideMainNavigation()
{
    toggleDisplay('.main_nav', false);
}

function hideFooter()
{
    toggleDisplay('footer', false);
}

function showNavigationAndFooter()
{
    showMainNavigation();
    showFooter();
}
