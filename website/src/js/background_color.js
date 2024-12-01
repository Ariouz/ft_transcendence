var INITIAL_BACKGROUND_COLOR;

function storeInitialWebsiteBackgroundColor() {
    const pageContainer = document.querySelector('.page_content_container');
    if (pageContainer) {
        const computedStyle = getComputedStyle(pageContainer);
        INITIAL_BACKGROUND_COLOR = computedStyle.backgroundColor;
    }
}

function resetWebsiteBackgroundColorToInitial() {
    const pageContainer = document.querySelector('.page_content_container');
    if (pageContainer && INITIAL_BACKGROUND_COLOR) {
        pageContainer.style.backgroundColor = INITIAL_BACKGROUND_COLOR;
    }
}

function setWebsiteBackgroundColor(color) {
    const pageContainer = document.querySelector('.page_content_container');
    if (pageContainer && color) {
        pageContainer.style.backgroundColor = color;
    }
}

storeInitialWebsiteBackgroundColor();
