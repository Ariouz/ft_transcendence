const DEFAULT_LANGUAGE = 'en';

// TODO remove this preference when removing user's data (GDPR)
function setLanguagePreference(lang) {
    localStorage.setItem('language', lang);
    location.reload();
}

function getLanguagePreference() {
    return localStorage.getItem('language') || DEFAULT_LANGUAGE;
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
    try {
        await setLanguagePreference(lang);
    } catch (error) {
        console.error('Error changing language:', error);
    }
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
    const availableLanguages = await fetchAvailableLanguages();
    const userPreferredLanguage = getLanguagePreference();
    const select = document.getElementById('settings_user_lang');
    select.onchange = function () {
        const selectedLang = this.value;
        changeLanguage(selectedLang);
    };
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
    const userPreferredLanguage = getLanguagePreference();
    const langData = await fetchLanguageData(userPreferredLanguage);
    const defaultLangData = userPreferredLanguage !== DEFAULT_LANGUAGE ?
        await fetchLanguageData(DEFAULT_LANGUAGE) : langData;
    updateContent(langData, defaultLangData);
}

function updateContent(langData, defaultLangData) {
    updateTextsI18n(langData, defaultLangData);
    updatePlaceholdersI18n(langData, defaultLangData);
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
