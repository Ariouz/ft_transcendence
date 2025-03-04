function highlightNav(item) {
    const settings_nav_item = document.getElementById(item);
    settings_nav_item.classList.add("settings_nav_highlighted");
}

function removeNavHighlight(items) {
    items.forEach(item => {
        const settings_nav_item = document.getElementById(item);
        settings_nav_item.classList.remove("settings_nav_highlighted");
    });
}

function showSection(section, title_i18n_ref, nav_item) {
    const sections = ["settings_profile_section", "settings_confidentiality_section", "settings_account_section"];
    const nav_items = ["settings_nav_profile", "settings_nav_confidentiality", "settings_nav_account"];

    hideError();
    hideSuccess();

    sections.forEach(sec => {
        document.getElementById(sec).style.display = 'none';
    });
    document.getElementById(section).style.display = 'flex';

    removeNavHighlight(nav_items);
    highlightNav(nav_item);

    document.getElementById("settings_section_title").setAttribute('data-i18n', title_i18n_ref);
    updateI18nOnNewPage();
}

function showProfileSection() {
    showSection("settings_profile_section", "profile_settings", "settings_nav_profile");

    let form = document.getElementById("settings_panel_form_profile")
    form.action = `https://${g_host}:8001/api/account/settings/profile/`+getCookie("session_token") + "/";

    form.addEventListener('submit', function(event) {
        showLoadingWheel();
        event.preventDefault();
        const formData = new FormData(this);

        postWithCsrfToken(this.action, formData)
        .then(data => {
            hideLoadingWheel();
            if (data.error)
                showError(data.error, data.details);
            else
                showSuccess(data.success)
        })
        .catch(error => {
            showError(error.error, error.details);
            hideLoadingWheel();
        })

        const langSelect = document.getElementById("settings_user_lang");
        const selectedLang = langSelect.value;
        changeLanguage(selectedLang);
    });
}

async function showConfidentialitySection() {
    showSection("settings_confidentiality_section", "confidentiality_settings", "settings_nav_confidentiality");

    let form = document.getElementById("settings_panel_form_confidentiality")
    form.action = `https://${g_host}:8001/api/account/settings/confidentiality/`+getCookie("session_token") + "/";

    form.addEventListener('submit', function(event) {
        showLoadingWheel();
        event.preventDefault();
        const formData = new FormData(this);

        postWithCsrfToken(this.action, formData)
        .then(data => {
            hideLoadingWheel();
            if (data.error)
                showError(data.error, data.details);
            else
                showSuccess(data.success);

            if (formData.has("revoke_cookies"))
                revokeAllCookies();
        })
        .catch(error => {
            showError(error.error, error.details);
            hideLoadingWheel();
        })
    });
}

async function showAccountSection() {
    showSection("settings_account_section", "account_settings", "settings_nav_account");

    let form = document.getElementById("settings_panel_form_account")
    form.action = `https://${g_host}:8001/api/account/settings/delete/`+getCookie("session_token") + "/";

    let userIdReq = await retrieveId(getCookieAcccessToken());
    if (userIdReq.error) return ;
    let userId = userIdReq.user_id;

    form.addEventListener('submit', function(event) {
        showLoadingWheel();
        event.preventDefault();
        const formData = new FormData(this);
        postWithCsrfToken(this.action, formData)
        .then(data => {
            postWithCsrfToken(`https://${g_host}:8002/api/account/settings/delete/`, {user_id:userId}, true)
            .catch(error => showNotification(error, 5));


            hideLoadingWheel();
            if (data.error)
                showError(data.error, data.details);
            else
            {
                logout();
                window.location.reload();
            }
        })
        .catch(error => {
            showError(error.error, error.details);
            hideLoadingWheel();
        })
    });
}

function hideElement(elementId) {
    document.getElementById(elementId).style.display = 'none';
}

function showElement(elementId, titleId, contentId, title, message) {
    hideElement('settings_error_div');
    hideElement('settings_success_div');
    
    let element = document.getElementById(elementId);
    element.style.display = 'block';

    document.getElementById(titleId).innerText = title;
    document.getElementById(contentId).innerText = message;
}

function hideError() {
    hideElement('settings_error_div');
}

function showError(title, message) {
    showElement('settings_error_div',
        'settings_error_title',
        'settings_error_content',
        title,
        message);
}

function hideSuccess() {
    hideElement('settings_success_div');
}

async function showSuccess(message) {
    showElement('settings_success_div',
        'settings_success_title',
        'settings_success_content',
        await getSentenceFromCode("success"),
        await getSentenceFromCode(message));
}

function showLoadingWheel()
{
    let wheel = document.getElementById("settings_loading_wheel");
    wheel.style.display = 'block';
    wheel.style.opacity = "50%";
}

function hideLoadingWheel()
{
    let wheel = document.getElementById("settings_loading_wheel");
    wheel.style.opacity = "0%";
    setTimeout(() => {
        wheel.style.display = 'none';
    }, 500);
}

function setInputValue(inputId, value)
{
    let input = document.getElementById(inputId);
    input.value = value;
}

function setSelected(inputId, value)
{
    let input = document.getElementById(inputId);
    input.selected = value;
}

function setChecked(inputId, value)
{
    let input = document.getElementById(inputId);
    input.checked = value;
}

function setDefaultSettingsValues()
{
    let token = getCookie("session_token");
    retrieveSettings(token)
        .then(userData => {
            if (userData.error)
            {
                logout();
                navigate("/login");
            }
            else
            {   
                setInputValue("settings_user_displayname", userData.display_name);
                setInputValue("settings_user_github", userData.github === "null" ? "" : userData.github);
                setInputValue("settings_user_status", userData.status_message);
                setInputValue("settings_user_lang", userData.lang);
                changeLanguage(userData.lang);


                retrieveConfidentialitySettings(token)
                .then(userConfidentiality => {
                    if (userConfidentiality.error) {
                        throw userConfidentiality.error;
                    }
                    setSelected("profile_visibility_"+userConfidentiality.profile_visibility, true);

                    setChecked("profile_show_fullname", userConfidentiality.show_fullname);
                    setChecked("profile_show_email", userConfidentiality.show_email);
                })
                .catch(error => {  });
            }
        }).catch(error => {  });
}

showProfileSection();
setDefaultSettingsValues();
createLanguageDropdown();
