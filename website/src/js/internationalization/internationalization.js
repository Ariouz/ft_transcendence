async function updateLanguagePreferenceRemoval() {
    removeLanguagePreference();
    SELECTED_LANGUAGE = getDefaultLanguage();
    try {
        updateI18nOnNewPage();
    } catch (error) {
    }
}

async function getSentenceFromCode(code) {
    return await fetchTranslation(code);
}

function getPreferredLanguageFromNavigator() {
    const userLanguages = navigator.languages;
    for (const userLang of userLanguages) {
        const langCode = userLang.includes('-') ? userLang.split('-')[0] : userLang;
        const isLanguageSupported = availableLanguages.some(lang => lang.code === langCode);
        if (isLanguageSupported) {
            return langCode;
        }
    }
    return DEFAULT_LANGUAGE;
}

async function changeLanguage(lang) {
    if (lang === SELECTED_LANGUAGE)
        return;
    try {
        setLanguagePreference(lang);
        await updateTranslations();
        await updateI18nOnNewPage();
    } catch (error) {
        console.error('Error changing language:', error);
    }
}

function setUserLanguage() {
    let token = getCookie("session_token");
    retrieveSettings(token)
        .then(userData => {
            if (!userData.error) {
                changeLanguage(userData.lang);
            }
        }).catch(error => {
        });
}

async function fetchAvailableLanguages() {
    try {
        const url = `https://localhost:8006/languages/`;
        const response = await fetch(url);
        if (!response.ok) {
            return null;
        }
        return await response.json();
    } catch (error) {
        return null;
    }
}

async function getLanguageDisplayName(languageCode) {
    try {
        const language = availableLanguages.find(lang => lang.code === languageCode);
        if (!language) {
            throw new Error(`Language with code ${languageCode} not found`);
        }
        return language.displayName;
    } catch (error) {
        // Todo
        return "An error occured";
    }
}

async function loadInitialTranslations() {
    DEFAULT_LANGUAGE = (await getDefaultI18nServiceLanguage()) || DEFAULT_LANGUAGE;
    let availableLanguagesResponse = await fetchAvailableLanguages();
    availableLanguages = availableLanguagesResponse == null ? null : availableLanguagesResponse.languages;

    SELECTED_LANGUAGE = localStorage.getItem('language') || getDefaultLanguage();
    await updateI18nOnNewPage();
}

async function updateTranslations() {
    SELECTED_LANGUAGE = getLanguagePreference();
}

async function fetchTranslation(key) {
    const translation = await fetchTranslationSelectedLanguage(key);
    if (translation) {
        return translation;
    } else {
        return await fetchTranslationDefaultLanguage(key);
    }
}

async function fetchTranslationDefaultLanguage(key) {
    try {
        const url = `https://localhost:8006/translations/${DEFAULT_LANGUAGE}/${key}/`;
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Error fetching translation: ${response.statusText}`);
        }
        const data = await response.json();
        return data[key];
    } catch (error) {
        // TODO
        return null;
    }
}

async function fetchTranslationSelectedLanguage(key) {
    try {
        const url = `https://localhost:8006/translations/${SELECTED_LANGUAGE}/${key}/`;
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Error fetching translation: ${response.statusText}`);
        }
        const data = await response.json();
        return data[key];
    } catch (error) {
        // TODO
        return null;
    }
}

async function fetchTranslationWithArgs(key, args = []) {
    const translation = await fetchTranslationSelectedTranslationWithArgs(key, args);
    if (translation) {
        return translation;
    } else {
        return await fetchTranslationDefaultLanguageWithArgs(key, args);
    }
}

async function fetchTranslationSelectedTranslationWithArgs(key, args = []) {
    try {
        const queryString = args.map(arg => `arg=${encodeURIComponent(arg)}`).join('&');
        const url = `https://localhost:8006/translations/${SELECTED_LANGUAGE}/${key}/?${queryString}`;
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Error fetching translation: ${response.statusText}`);
        }
        const data = await response.json();
        return data[key];
    } catch (error) {
        // TODO
        return null;
    }
}

async function fetchTranslationDefaultLanguageWithArgs(key, args = []) {
    try {
        const queryString = args.map(arg => `arg=${encodeURIComponent(arg)}`).join('&');
        const url = `https://localhost:8006/translations/${DEFAULT_LANGUAGE}/${key}/?${queryString}`;
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Error fetching translation: ${response.statusText}`);
        }
        const data = await response.json();
        return data[key];
    } catch (error) {
        // TODO
        return null;
    }
}


loadInitialTranslations();
