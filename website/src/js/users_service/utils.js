function setCookie(name, value, days=7, seconds=null) {
    let expires = "";
    let date = new Date();
    if (seconds) {
        date.setTime(date.getTime() + (seconds * 1000));
    } else if (days) {
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    }
    expires = "; expires=" + date.toUTCString();
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    let nameEQ = name + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}