const PONG_DEFAULT_STYLES = getRootFromSpecificCSS("pong_game.css");
console.log(PONG_DEFAULT_STYLES);

function getRootFromSpecificCSS(cssFileName) {
    const result = {};

    for (let sheet of document.styleSheets) {
        if (sheet.href && sheet.href.includes(cssFileName)) {
            try {
                for (let rule of sheet.cssRules) {
                    if (rule.selectorText === ":root") {
                        for (let i = 0; i < rule.style.length; i++) {
                            const property = rule.style[i];
                            const value = rule.style.getPropertyValue(property);
                            result[property] = value.trim();
                        }
                    }
                }
            } catch (error) {
            }
        }
    }
    return result;
}

function setArcadeTheme(theme) {
    changeTheme(theme);
}

function resetTheme() {
    changeTheme(PONG_DEFAULT_STYLES);
}

function changeTheme(theme) {
    for (let [key, value] of Object.entries(theme)) {
        document.documentElement.style.setProperty(key, value);
    }
}
