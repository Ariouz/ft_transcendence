import ft_requests
import os
import json
import time

I18N_URL = "http://i18n-service:8006"
DEFAULT_LOCALE_DIR = "locale"
I18N_DEFAULT_LANGUAGE = 'en'

def fetch_translation(lang, key):
    """
    Raises:
        ft_requests.exceptions.RequestException
    """
    url = f"{I18N_URL}/translations/{lang}/{key}/"
    response = ft_requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get(key, None)


def get_translation(lang, key, *args):
    fallback_languages = [
        lang,
        os.getenv('DEFAULT_LANGUAGE_CODE'),
        I18N_DEFAULT_LANGUAGE
    ]
    
    translation = None
    
    for fallback_lang in fallback_languages:
        if not fallback_lang:
            continue
        try:
            translation = fetch_translation(fallback_lang, key)
            if translation:
                break
        except Exception:
            pass
        translation = get_translation_from_locale_file(fallback_lang, key)
        if translation:
            break

    if translation is None:
        return key
    if args:
        try:
            translation = translation % args
        except Exception:
            return key
    
    return translation


def fetch_available_languages():
    """
    Raises:
        ft_requests.exceptions.RequestException
    """
    url = f"{I18N_URL}/languages/"
    response = ft_requests.get(url)
    response.raise_for_status()
    languages_data = response.json()
    languages = [lang["code"] for lang in languages_data.get("languages", [])]
    return languages


def get_translation_from_locale_file(lang, key):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        locale_dir = os.path.join(current_dir, DEFAULT_LOCALE_DIR)

        filename = f"{lang}.json"
        json_file_path = os.path.join(locale_dir, filename)

        if os.path.exists(json_file_path):
            try:
                with open(json_file_path, "r", encoding="utf-8") as json_file:
                    data = json.load(json_file)
                    return data.get(key, None)
            except Exception:
                return None
        else:
            return None
    except Exception:
        return None

def get_preferred_language(request=None, default_language_code=I18N_DEFAULT_LANGUAGE):
    if request == None:
        return default_language_code
    accept_language = request.META.get("HTTP_ACCEPT_LANGUAGE", "")
    if not accept_language:
        return default_language_code
    try:
        available_languages = fetch_available_languages()
    except Exception:
        return default_language_code
    if not available_languages:
        return default_language_code
    user_languages = [lang.split(";")[0] for lang in accept_language.split(",")]
    for user_lang in user_languages:
        lang_code = user_lang.split("-")[0] if "-" in user_lang else user_lang
        if lang_code in available_languages:
            return lang_code
    return default_language_code
