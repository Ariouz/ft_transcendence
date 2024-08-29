const DEFAULT_LANGUAGE = 'en';
let SELECTED_LANGUAGE = DEFAULT_LANGUAGE;
let selectedLanguageData = {};
let defaultLanguageData = {};
let availableLanguages = {};

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
        selectedLanguageData = await fetchLanguageData(SELECTED_LANGUAGE);
        updateI18nOnNewPage();
    } catch (error) {
    }
}

function getSentenceFromLanguageCode(code) {
    return selectedLanguageData[code] || defaultLanguageData[code];
}

function getLanguageDisplayName(code) {
    let language = availableLanguages.find(lang => lang.code === code);
    if (!language) {
        language = availableLanguages.find(lang => lang.code === 'en');
    }
    return language ? language.displayName : `Failed to load language data for ${code}`;
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


async function fetchLanguageData(lang) {
    try {
        const response = await fetch(`/assets/lang/${lang}.json`);
        return await response.json();
    } catch (error) {
        console.error(`Failed to load language data for ${lang}:`, error);
        return {};
    }
}

async function changeLanguage(lang) {
    if (lang === SELECTED_LANGUAGE)
        return;
    try {
        setLanguagePreference(lang);
        // TODO send to server new language preference
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
        const response = await fetch('/assets/lang/languages.json');
        const data = await response.json();
        return data.languages;
    } catch (error) {
        console.error('Failed to load languages list:', error);
        return [];
    }
}

async function createLanguageDropdown() {
    const userPreferredLanguage = getLanguagePreference();
    const select = document.getElementById('settings_user_lang');
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
    updateContent();
}

function updateContent() {
    updateTextsI18n(selectedLanguageData, defaultLanguageData);
    updatePlaceholdersI18n(selectedLanguageData, defaultLanguageData);
}

function updateTextsI18n(langData, defaultLangData) {
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        element.innerHTML = langData[key] || defaultLangData[key];
    });
}

function updatePlaceholdersI18n(langData, defaultLangData) {
    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        const placeholderText = langData[key] || defaultLangData[key];
        element.setAttribute('placeholder', placeholderText);
    });
}

async function loadInitialTranslations() {
    availableLanguages = await fetchAvailableLanguages();
    const userPreferredLanguage = localStorage.getItem('language') || getDefaultLanguage();
    SELECTED_LANGUAGE = userPreferredLanguage;
    selectedLanguageData = await fetchLanguageData(userPreferredLanguage);
    if (userPreferredLanguage !== DEFAULT_LANGUAGE) {
        defaultLanguageData = await fetchLanguageData(DEFAULT_LANGUAGE);
    } else {
        defaultLanguageData = selectedLanguageData;
    }
    updateContent(selectedLanguageData);
}

async function updateTranslations() {
    const userPreferredLanguage = getLanguagePreference();
    if (userPreferredLanguage === SELECTED_LANGUAGE)
        return;
    SELECTED_LANGUAGE = userPreferredLanguage;
    selectedLanguageData = await fetchLanguageData(userPreferredLanguage);
}

loadInitialTranslations();
