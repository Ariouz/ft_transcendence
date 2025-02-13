async function getDefaultI18nServiceLanguage() {
    if (await isTranslationServiceOffline()) return null;
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

function getDefaultLanguage() {
    return getPreferredLanguageFromNavigator() || DEFAULT_LANGUAGE;
}
