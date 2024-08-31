import os
import json
from django.conf import settings

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def load_translation(lang_code):
    file_path = os.path.join(settings.BASE_DIR, 'i18n_service_app', 'locales', f'{lang_code}.json')
    return load_json_file(file_path)

def load_languages():
    file_path = os.path.join(settings.BASE_DIR, 'i18n_service_app', 'locales', 'languages.json')
    return load_json_file(file_path)
