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

    sections.forEach(sec => document.getElementById(sec).style.display = 'none');
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

function hideError()
{
    errorDiv = document.getElementById("settings_error_div");
    errorDiv.style.display = 'none';
}

function showError(title, message)
{
    hideSuccess();
    errorDiv = document.getElementById("settings_error_div");
    errorDiv.style.display = 'block';

    errorTitle = document.getElementById("settings_error_title");
    errorContent = document.getElementById("settings_error_content");

    errorTitle.innerText = title;
    errorContent.innerText = message;
}

function hideSuccess()
{
    successDiv = document.getElementById("settings_success_div");
    successDiv.style.display = 'none';
}

function showSuccess(title, message)
{
    hideError();
    successDiv = document.getElementById("settings_success_div");
    successDiv.style.display = 'block';

    successTitle = document.getElementById("settings_success_title");
    successContent = document.getElementById("settings_success_content");

    successTitle.innerText = title;
    successContent.innerText = message;
}

function showLoadingWheel()
{
    wheel = document.getElementById("settings_loading_wheel");
    wheel.style.display = "block";
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

showProfileSection();
hideError();
hideSuccess();