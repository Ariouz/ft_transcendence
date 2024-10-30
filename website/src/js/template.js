
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
