const FT_AUTH_URL = "http://localhost:8001/api/auth/42";

function showError(error)
{
    console.log(error);
}

function redirectToAuth(data)
{
    console.log(data.url);
    window.location.replace(data.url);
}

async function accountExists(username, token)
{
    let url = `http://localhost:8001/api/account/exists/?username=${username}&token=${token}`;
    let data = await fetchBack(url)
    .then(data => {
        console.log(data);
        return data.exists;
    }).catch(error => {
        console.error(error);
        return false;
    });
    return data;
}

async function createAccount(username, email, token)
{
    if (await accountExists(username, token)){
        console.log("Account exists, skip creation");
        setCookie("session_token", token_data.access_token, 0, token_data.expires_in);
        navigate('/');
        window.location.reload();
        return ;
    }
    let url = `http://localhost:8001/api/account/create/?username=${username}&email=${email}&token=${token}`;
    let data = fetchBack(url)
    .then(data => {
        console.log(data);
        setCookie("session_token", token_data.access_token, 0, token_data.expires_in);
        navigate('/');
        window.location.reload();
    })
    .catch(error => {
        console.error(error)
    });
}

async function ftGetAccess()
{
    url = `${FT_AUTH_URL}`;
    getFromURL(url, redirectToAuth, showError);
}

async function retrieveUsername(access_token)
{
    const url = `${FT_AUTH_URL}/data/username/${access_token}`;
    try {
        const data = await fetchBack(url);
        console.log(data);
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
        console.log(data);
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
    const url = `${FT_AUTH_URL}/access/?code=${code}`;
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