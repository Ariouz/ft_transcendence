from django.conf import settings
import ft_i18n
from django.http import JsonResponse


def json_response(data, status_code=200):
    return JsonResponse(data, status=status_code)


def get_translation(request, string, *args):
    ft_i18n.get_translation(ft_i18n.get_preferred_language(request, settings.USERS_DEFAULT_LANGUAGE_CODE), string, args)


def success_response(request, success_title, status_code=200, extra_data=None, translate=True):
    response_data = {
        "success": ft_i18n.get_translation(ft_i18n.get_preferred_language(request, settings.USERS_DEFAULT_LANGUAGE_CODE), success_title) if translate else success_title
    }
    if extra_data:
        response_data.update(extra_data)
    
    return JsonResponse(response_data, status=status_code)


def error_response(request, error_title, details, status_code=400):
    language = ft_i18n.get_preferred_language(request, settings.USERS_DEFAULT_LANGUAGE_CODE)
    return JsonResponse(
        {
            "error": ft_i18n.get_translation(language, error_title),
            "details": ft_i18n.get_translation(language, details),
        },
        status = status_code
    )
