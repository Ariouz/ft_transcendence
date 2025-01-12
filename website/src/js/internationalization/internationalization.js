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
    if (availableLanguages == null)
        return DEFAULT_LANGUAGE;
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
    if (isOfflineTimestampValid() || await isTranslationServiceOffline()) return null;

    try {
        const url = `https://${g_host}:8006/languages/`;
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
    if (availableLanguages == null)
        return languageCode;
    try {
        const language = availableLanguages.find(lang => lang.code === languageCode);
        if (!language) {
            return languageCode;
        }
        return language.displayName;
    } catch (error) {
        return languageCode;
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

function isOfflineTimestampValid() {
    const offlineTimestamp = sessionStorage.getItem("I18N_SERVICE_OFFLINE_TIMESTAMP");

    if (!offlineTimestamp) {
        return null;
    }

    const offlineTime = new Date(parseInt(offlineTimestamp, 10));
    const now = new Date();
    return now - offlineTime < I18N_SERVICE_OFFLINE_TIMER;
}


async function isTranslationServiceOffline() {
    timeoutNotFinished = isOfflineTimestampValid();
    if (timeoutNotFinished != null) {
        return timeoutNotFinished;
    }
    try {
        await testTranslationService();
        return false;
    } catch (error) {
        return true;
    }
}

let isTestTranslationServiceRunning = false;
let testTranslationPromise = null;

async function testTranslationService() {
    if (isTestTranslationServiceRunning) {
        return testTranslationPromise;
    }

    timeoutNotFinished = isOfflineTimestampValid();
    if (timeoutNotFinished != null) {
        return timeoutNotFinished;
    }

    isTestTranslationServiceRunning = true;
    testTranslationPromise = (async () => {
        try {
            const testUrl = `${I18N_SERVICE_URL}/default-language/`;

            const response = await fetch(testUrl, { method: 'HEAD' });

            if (!response || !response.ok) {
                sessionStorage.setItem("I18N_SERVICE_OFFLINE_TIMESTAMP", Date.now().toString());
                throw new Error();
            }
        } catch (error) {
            sessionStorage.setItem("I18N_SERVICE_OFFLINE_TIMESTAMP", Date.now().toString());
            throw new Error();
        } finally {
            isTestTranslationServiceRunning = false;
            testTranslationPromise = null;
        }
    })();

    sessionStorage.removeItem("I18N_SERVICE_OFFLINE_TIMESTAMP");
    return testTranslationPromise;
}


async function fetchTranslation(key) {
    if (isOfflineTimestampValid()) {
        return await fetchTranslationFromLocal(key) || key;
    } else {
        var checkIsOffline = await isTranslationServiceOffline();
        if (checkIsOffline == true)
            return await fetchTranslationFromLocal(key) || key;
    }
    try {
        const translation = await fetchTranslationSelectedLanguage(key);
        if (translation) {
            return translation;
        }
        const defaultTranslation = await fetchTranslationDefaultLanguage(key);
        if (defaultTranslation) {
            return defaultTranslation;
        }
        const localTranslation = await fetchTranslationFromLocal(key);
        return localTranslation || key;
    } catch (error) {
        return await fetchTranslationFromLocal(key) || key;
    }
}

async function fetchTranslationDefaultLanguage(key) {
    try {
        const url = `https://${g_host}:8006/translations/${DEFAULT_LANGUAGE}/${key}/`;
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error();
        }
        const data = await response.json();
        return data[key];
    } catch (error) {
        throw new Error();
    }
}

async function fetchTranslationSelectedLanguage(key) {
    try {
        const url = `https://${g_host}:8006/translations/${SELECTED_LANGUAGE}/${key}/`;
        const response = await fetch(url);
        if (!response.ok) {
            return key;
        }
        const data = await response.json();
        if (data.error) {
            throw new Error();
        }
        return data[key];
    } catch (error) {
        throw new Error();
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
        const url = `https://${g_host}:8006/translations/${SELECTED_LANGUAGE}/${key}/?${queryString}`;
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
        const url = `https://${g_host}:8006/translations/${DEFAULT_LANGUAGE}/${key}/?${queryString}`;
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
