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

function showSection(section, title, nav_item) {
    const sections = ["settings_profile_section", "settings_friends_section", "settings_confidentiality_section", "settings_account_section"];
    const nav_items = ["settings_nav_profile", "settings_nav_friends", "settings_nav_confidentiality", "settings_nav_account"];

    sections.forEach(sec => {
        document.getElementById(sec).style.display = 'none';
    });
    document.getElementById(section).style.display = 'flex';

    removeNavHighlight(nav_items);
    highlightNav(nav_item);

    document.getElementById("settings_section_title").innerText = title;
}

function showProfileSection() {
    showSection("settings_profile_section", "Profile Settings", "settings_nav_profile");

    form = document.getElementById("settings_panel_form_profile")
    form.action = "http://localhost:8001/api/account/settings/profile/"+getCookie("session_token");

    form.addEventListener('submit', function(event) {
        showLoadingWheel();
        event.preventDefault();
        const formData = new FormData(this);

        fetch(this.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            hideLoadingWheel();
            if (data.error)
                showError(data.error, data.details);
            else
                showSuccess("Success", "Your profile data has been saved!")
        })
        .catch(error => {
            showError(error.error, error.details);
            hideLoadingWheel();
        })
    });
}

function showFriendsSection() {
    showSection("settings_friends_section", "Friends Settings", "settings_nav_friends");
}

function showConfidentialitySection() {
    showSection("settings_confidentiality_section", "Confidentiality Settings", "settings_nav_confidentiality");
}

function showAccountSection() {
    showSection("settings_account_section", "Account Settings", "settings_nav_account");
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
    showElement('settings_error_div', 'settings_error_title', 'settings_error_content', title, message);
}

function hideSuccess() {
    hideElement('settings_success_div');
}

function showSuccess(title, message) {
    showElement('settings_success_div', 'settings_success_title', 'settings_success_content', title, message);
}

function showLoadingWheel()
{
    wheel = document.getElementById("settings_loading_wheel");
    wheel.style.display = 'block';
    wheel.style.opacity = "50%";
}

function hideLoadingWheel()
{
    wheel = document.getElementById("settings_loading_wheel");
    wheel.style.opacity = "0%";
    setTimeout(() => {
        wheel.style.display = 'none';
    }, 500);
}

function selectDefaultLanguage(lang)
{
    select = document.getElementById("settings_user_lang");

    for (let i = 0; i < select.options.length; i++)
    {
        if (select.options[i].value == lang){
            select.selectedIndex = i;
            break; 
        }
    }
}

function setInputValue(inputId, value)
{
    input = document.getElementById(inputId);
    input.value = value;
}

function setDefaultProfileSettingsValues()
{
    token = getCookie("session_token");
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
                setInputValue("settings_user_github", userData.github);
                setInputValue("settings_user_status", userData.status_message);
                selectDefaultLanguage(userData.lang);    
            }
        }).catch(error => {console.error(error);});
}

showProfileSection();
hideError();
hideSuccess();
setDefaultProfileSettingsValues();