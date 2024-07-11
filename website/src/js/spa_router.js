function handleRouting() {
    const path = window.location.pathname;
    
    if (path === '/pong') {
        loadContent("/pages/pong.html");
    }
    else if (path === '/') {
        loadContent("/pages/home.html");
    }
    else {
        loadContent("/pages/error/404.html");
    }
}

function loadContent(url) {
    fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(html => {
        document.getElementById('page_content').innerHTML = html;
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

handleRouting();

window.addEventListener('popstate', handleRouting);

function navigate(path) {
    history.pushState(null, null, path);
    handleRouting();
}
