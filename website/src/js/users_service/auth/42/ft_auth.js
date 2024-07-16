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

async function ftGetAccess()
{
    url = `${FT_AUTH_URL}`;
    getFromURL(url, redirectToAuth, showError);
}

async function retrieveFtData(code)
{
    url = `${FT_AUTH_URL}` + "/access/"+code;
    try {
        data = fetchBack(url);
        console.log(data);
    } catch (error)
    {
        console.log(error);
    }
}

async function fetchBack(url)
{
    try {
        const response = await fetch(url);
        const data = await response.json();

        if (response.ok) {
            console.debug('Data:', data);
            return data;
        } else {
            console.error('Error:', data);
            return data;
        }
    } catch (error) {
        throw error;
    }
}
