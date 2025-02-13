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
