const g_host = window.location.host.split(":")[0];


function setCookieBannerVisibility(mode, finalOpacity)
{
    cookieBanner = document.getElementById("cookie_consent_banner");
    cookieBanner.style.display = mode;
    setTimeout(() => {
        cookieBanner.style.opacity = finalOpacity;
    }, 500);
}

function acceptCookies()
{
    setCookieBannerVisibility('none', '0');
    setCookie("cookie_consent", true);
}
