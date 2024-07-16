const USERS_SERVICE_URL = "http://localhost:8001/api";

async function getUsers(onSuccess, onError)
{
    url = `${USERS_SERVICE_URL}/users`
    getFromURL(url, onSuccess, onError)
}

async function getFromURL(url, onSuccess, onError)
{
    try {
        const response = await fetch(url);

        const data = await response.json();

        if (response.ok) {
            console.debug('Data:', data);
            onSuccess(data);
        } else {
            console.error('Error:', data);
            onError(data);
        }
    } catch (error) {
        console.error('Error:', error);
        onError(error);
    }
}
