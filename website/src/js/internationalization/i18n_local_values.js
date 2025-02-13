async function fetchLocaleFromLocal(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            return null;
        }
        return await response.json();
    } catch (error) {
        return null;
    }
}

async function fetchTranslationFromLocal(key) {
    const url = "/assets/locale/en.json";
    try {
        const localeJson = await fetchLocaleFromLocal(url);
        return localeJson[key] || null;
    } catch (error) {
        return null;
    }
}
