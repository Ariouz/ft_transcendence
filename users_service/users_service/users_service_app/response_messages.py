from django.conf import settings
import ft_i18n
import ft_requests
from django.http import JsonResponse


def get_preferred_language(request):
    accept_language = request.META.get("HTTP_ACCEPT_LANGUAGE", "")
    if not accept_language:
        return settings.USERS_DEFAULT_LANGUAGE_CODE
    try:
        available_languages = ft_i18n.fetch_available_languages()
    except Exception as e:
        return settings.USERS_DEFAULT_LANGUAGE_CODE
    if not available_languages:
        return settings.USERS_DEFAULT_LANGUAGE_CODE
    user_languages = [lang.split(";")[0] for lang in accept_language.split(",")]
    for user_lang in user_languages:
        lang_code = user_lang.split("-")[0] if "-" in user_lang else user_lang
        if lang_code in available_languages:
            return lang_code
    return settings.USERS_DEFAULT_LANGUAGE_CODE


def success_response(request, title):
    return JsonResponse(
        {"success": ft_i18n.get_translation(get_preferred_language(request), title)}
    )


def error_response(request, title, details):
    language = get_preferred_language(request)
    return JsonResponse(
        {
            "error": ft_i18n.get_translation(language, title),
            "details": ft_i18n.get_translation(language, details),
        }
    )
