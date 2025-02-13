async function createLanguageDropdown() {
    const userPreferredLanguage = getLanguagePreference();
    const select = document.getElementById('settings_user_lang');

    if (availableLanguages == null || Object.keys(availableLanguages).length == 0) {
        await loadInitialTranslations();
    }

    if (availableLanguages == null || Object.keys(availableLanguages).length == 0) {
        const errorOption = document.createElement("option");
        errorOption.textContent = await getSentenceFromCode("feature_not_available_error");
        errorOption.value = "error";
        select.disabled = true;
        select.appendChild(errorOption);

        select.disabled = true;
        return;
    }

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
