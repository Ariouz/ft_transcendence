function setLanguagePreference(lang) {
    localStorage.setItem('language', lang);
}

function getLanguagePreference() {
    return localStorage.getItem('language') || getDefaultLanguage();
}

async function removeLanguagePreference() {
    localStorage.removeItem('language');
}
