const USERS_SERVICE_URL = `https://${g_host}:8001/api`;

async function getUsers(onSuccess, onError)
{
    let url = `${USERS_SERVICE_URL}/users`
    getFromURL(url, onSuccess, onError)
}

async function getFromURL(url, onSuccess, onError)
{
    try {
        const response = await fetch(url);

        const data = await response.json();

        if (response.ok) {
            onSuccess(data);
        } else {
            onError(data);
        }
    } catch (error) {
        onError(error);
    }
}
