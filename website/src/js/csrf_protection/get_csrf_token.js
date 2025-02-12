async function fetchCsrfToken(port) {
    const response = await fetch(`https://${g_host}:${port}/api/get-csrf-token/`, {
        credentials: 'include',
    }).catch(async error => {
        await showUnavailableError();
    });
    const data = await response.json();
    return data.csrfToken;
}

async function fetchCsrfTokenFromService(url) {
    try {
        const parsedUrl = new URL(url);
        const port = parsedUrl.port || (parsedUrl.protocol === 'https:' ? '8443' : '8080');
        return fetchCsrfToken(port);
    } catch (error) {
        throw new Error('Failed to fetch CSRF token due to invalid URL');
    }
}
