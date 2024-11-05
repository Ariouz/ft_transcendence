var DEFAULT_LANGUAGE = 'en';
let SELECTED_LANGUAGE = DEFAULT_LANGUAGE;
let availableLanguages = {};
const I18N_SERVICE_URL = "http://localhost:8006"

async function assignDefaultLanguage() {
    const url = `${I18N_SERVICE_URL}/default-language/`;
    try {
        const data = await fetchBack(url);
        return data.default_language;
    } catch (error) {
        return {
            error: "Cannot fetch user data",
            details: error.message
        };
    }
}

function setLanguagePreference(lang) {
    localStorage.setItem('language', lang);
}

function getDefaultLanguage() {
    return getPreferredLanguageFromNavigator() || DEFAULT_LANGUAGE;
}

function getLanguagePreference() {
    return localStorage.getItem('language') || getDefaultLanguage();
}

async function removeLanguagePreference() {
    localStorage.removeItem('language');
    SELECTED_LANGUAGE = getDefaultLanguage();
    try {
        updateI18nOnNewPage();
    } catch (error) {
    }
}

function getSentenceFromCode(code) {
    return fetchTranslation(code);
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
        const url = `http://localhost:8006/languages/`;
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Error fetching languages: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        // TODO
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

async function createLanguageDropdown() {
    const userPreferredLanguage = getLanguagePreference();
    const select = document.getElementById('settings_user_lang');
    
    if (availableLanguages.length == 0) await loadInitialTranslations();

    availableLanguages.forEach(lang => {
        const option = document.createElement('option');
        option.value = lang.code;
        option.textContent = lang.displayName;
        if (lang.code === userPreferredLanguage) {
            option.selected = true;
        }
        select.appendChild(option);
    });
}

async function updateI18nOnNewPage() {
    updateTextsI18n();
    updatePlaceholdersI18n();
}

function updateTextsI18n() {
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translationPromise = fetchTranslation(key);
        translationPromise.then((text) => {
            element.innerHTML = text;
        })
    });
}

function updatePlaceholdersI18n() {
    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        const translationPlaceholderPromise = fetchTranslation(key);
        translationPlaceholderPromise.then((placeholderText) => {
            element.setAttribute('placeholder', placeholderText);
        })
    });
}

async function loadInitialTranslations() {
    DEFAULT_LANGUAGE = (await assignDefaultLanguage()) || DEFAULT_LANGUAGE;
    let availableLanguagesResponse = await fetchAvailableLanguages();
    availableLanguages = availableLanguagesResponse.languages;

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
        const url = `http://localhost:8006/translations/${DEFAULT_LANGUAGE}/${key}/`;
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
        const url = `http://localhost:8006/translations/${SELECTED_LANGUAGE}/${key}/`;
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
        const url = `http://localhost:8006/translations/${SELECTED_LANGUAGE}/${key}/?${queryString}`;
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
        const url = `http://localhost:8006/translations/${DEFAULT_LANGUAGE}/${key}/?${queryString}`;
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
