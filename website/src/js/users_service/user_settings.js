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

showProfileSection();