var DEFAULT_LANGUAGE = 'en';
let SELECTED_LANGUAGE = DEFAULT_LANGUAGE;
let availableLanguages = null;
const I18N_SERVICE_URL = `https://${g_host}:8006`;
const I18N_SERVICE_OFFLINE_TIMER_MINUTES = 10 * 60 * 1000;
