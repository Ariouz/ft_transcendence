from django.http import JsonResponse
from .utils import load_translation, load_languages

# https://stackoverflow.com/questions/34798703/creating-utf-8-jsonresponse-in-django
def utf8JsonResponse(data):
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})

def translations_view(request, lang_code):
    translations = load_translation(lang_code)
    return utf8JsonResponse(translations)

def translation_by_key_view(request, lang_code, key):
    try:
        translations = load_translation(lang_code)
        if not translations:
            return JsonResponse({'error': f'No translations found for language code: {lang_code}'}, status=404)
        if key in translations:
            translation = translations[key]
            format_args = request.GET.getlist('arg')
            if '%' in translation and not format_args:
                return JsonResponse({'error': 'Arguments required for formatting are missing.'}, status=400)
            try:
                formatted_translation = translation % tuple(format_args)
                return utf8JsonResponse({key: formatted_translation})
            except TypeError as e:
                return JsonResponse({'error': f'Incorrect number of arguments provided for formatting: {str(e)}'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': f'Error formatting translation: {str(e)}'}, status=400)
        else:
            return JsonResponse({'error': 'Translation key not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

def languages_view(request):
    languages = load_languages()
    return utf8JsonResponse(languages)
