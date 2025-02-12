const FT_AUTH_URL = `${USERS_SERVICE_URL}/auth/42`;

async function showUnavailableError()
{
    showNotification(await fetchTranslation("service_unavailable"), 5);
}

function redirectToAuth(data)
{
    window.location.replace(data.url);
}

async function accountExists(username, token)
{
    let url = `https://${g_host}:8001/api/account/exists/?username=${username}&token=${token}`;
    let data = await fetchBack(url)
    .then(data => {
        return data.exists;
    }).catch(error => {
        return false;
    });
    return data;
}

async function createAccount(username, email, token, avatar, fullname)
{
    if (await accountExists(username, token)){
        
        if (doConsentCookies())
        {
            setCookie("session_token", token_data.access_token, 0, token_data.expires_in);
            createWebSocketFriendList();
        }
        navigateToRedirectOr("/");
        window.location.reload();
        return ;
    }
    let url = `https://${g_host}:8001/api/account/create/?username=${username}&email=${email}&token=${token}&avatar=${avatar}&fullname=${fullname}`;
    fetchBack(url)
    .then(data => {
        if (doConsentCookies())
        {
            setCookie("session_token", token_data.access_token, 0, token_data.expires_in);
            createWebSocketFriendList();
        }
        navigateToRedirectOr("/");
        window.location.reload();
    })
    .catch(error => {
        console.log(error)
    });
}

async function ftGetAccess()
{
    setCookieBannerVisibility("none", "0");

    let url = `${FT_AUTH_URL}`;
    getFromURL(url, redirectToAuth, showUnavailableError);
}

async function retrieveUsername(access_token)
{
    const url = `${FT_AUTH_URL}/data/username/${access_token}`;
    try {
        const data = await fetchBack(url);
        return data;
    } catch (error)
    {
        return {
            error: "Cannot fetch user data",
            details: error.message
        };
    }
}

async function retrieveDisplayName(user_id)
{
    const url = `${FT_AUTH_URL}/data/displayname/${user_id}`;
    try {
        const data = await fetchBack(url);
        return data;
    } catch (error)
    {
        return {
            error: "Cannot fetch user data",
            details: error.message
        };
    }
}

async function retrieveId(access_token)
{
    const url = `${FT_AUTH_URL}/data/id/${access_token}`;
    try {
        const data = await fetchBack(url);
        return data;
    } catch (error)
    {
        return {
            error: "Cannot fetch user data",
            details: error.message
        };
    }
}

async function retrieveSettings(access_token)
{
    const url = `${FT_AUTH_URL}/data/settings/${access_token}`;
    try {
        const data = await fetchBack(url);
        return data;
    } catch (error)
    {
        return {
            error: "Cannot fetch user data",
            details: error.message
        };
    }
}

async function retrieveConfidentialitySettings(access_token)
{
    const url = `${FT_AUTH_URL}/data/settings/confidentiality/${access_token}`;
    try {
        const data = await fetchBack(url);
        return data;
    } catch (error)
    {
        return {
            error: "Cannot fetch user data",
            details: error.message
        };
    }
}

async function retrievePublicProfileDataByUsername(username)
{
    const url = `${USERS_SERVICE_URL}/user/profile/data/${username}`;
    try {
        const data = await fetchBack(url);
        return data;
    } catch (error)
    {
        return {
            error: "Cannot fetch user data",
            details: error.message
        };
    }
}

async function retrievePublicProfileDataById(userId)
{
    const url = `${USERS_SERVICE_URL}/user/profile/data/id/${userId}`;
    try {
        const data = await fetchBack(url);
        return data;
    } catch (error)
    {
        return {
            error: "Cannot fetch user data",
            details: error.message
        };
    }
}

async function retrieveAllUsers()
{
    const url = `${USERS_SERVICE_URL}/users/all/data`;
    try {
        const data = await fetchBack(url);
        return data;
    } catch (error)
    {
        return {
            error: "Cannot fetch user data",
            details: error.message
        };
    }
}

async function retrieveFtData(access_token)
{
    const url = `${FT_AUTH_URL}/data/42/${access_token}`;
    try {
        const data = await fetchBack(url);
        return data;
    } catch (error)
    {
        return {
            error: "Cannot fetch user data",
            details: error.message
        };
    }
}

async function ftRetrieveClientAccessToken(code)
{
    const url = `${FT_AUTH_URL}/access?code=${code}`;
    try {
        const data = await fetchBack(url);
        return data;
    } catch (error)
    {
        return {
            error: "Cannot fetch access token",
            details: error.message
        };
    }
}

function getCookieAcccessToken()
{
    return getCookie("session_token");
}