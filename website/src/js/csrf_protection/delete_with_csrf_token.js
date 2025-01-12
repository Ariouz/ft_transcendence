function deleteWithCsrfToken(url, bodyContent = null, isJson = false) {
    return fetchCsrfTokenFromService(url)
        .then(csrfToken => {
            const options = {
                method: 'DELETE',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Referer': 'https://127.0.0.1:8443',
                },
            };
            if (isJson) {
                options.headers['Content-Type'] = 'application/json';
                if (bodyContent) {
                    options.body = JSON.stringify(bodyContent);
                }
            } else {
                if (bodyContent) {
                    options.body = bodyContent;
                }
            }
            return fetch(url, options);
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(errorText => {
                    throw new Error(`HTTP ${response.status}: ${errorText}`);
                });
            }
            return response.json().catch(() => ({}));
        });
}
