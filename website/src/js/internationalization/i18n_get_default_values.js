async function getDefaultI18nServiceLanguage() {
    const url = `${I18N_SERVICE_URL}/default-language/`;
    try {
        const data = await fetchBack(url);
        return data.default_language;
    } catch (error) {
        throw new Error();
    }
}

function getDefaultLanguage() {
    return getPreferredLanguageFromNavigator() || DEFAULT_LANGUAGE;
}
