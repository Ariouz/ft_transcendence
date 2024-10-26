import ft_requests
import os
import json

I18N_URL = "http://i18n-service:8006"
DEFAULT_LOCALE_DIR = "locale"


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


def get_translation(lang, key):
    try:
        translation = fetch_translation(lang, key)
        if translation == None:
            translation = get_translation_from_locale_file(lang, key)
            if translation == None:
                return key
        return translation
    except Exception as e:
        try:
            translation = get_translation_from_locale_file(key)
            if translation == None:
                return key
            return translation
        except Exception as e:
            return key


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


def get_translation_from_locale_file(key):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    locale_dir = os.path.join(current_dir, DEFAULT_LOCALE_DIR)

    for filename in os.listdir(locale_dir):
        if filename.endswith(".json"):
            json_file_path = os.path.join(locale_dir, filename)
            with open(json_file_path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                return data.get(key, None)
    return None
