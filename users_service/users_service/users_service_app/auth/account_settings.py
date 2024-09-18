from users_service_app.models import *
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import os
from django.conf import settings
import ft_i18n
import ft_requests


def get_preferred_language(request):
    accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    if not accept_language:
        return settings.USERS_DEFAULT_LANGUAGE_CODE
    try:
        available_languages = ft_i18n.fetch_available_languages()
    except ft_requests.exceptions.RequestException as e:
        return settings.USERS_DEFAULT_LANGUAGE_CODE
    if not available_languages:
        return settings.USERS_DEFAULT_LANGUAGE_CODE
    user_languages = [lang.split(';')[0] for lang in accept_language.split(',')]
    for user_lang in user_languages:
        lang_code = user_lang.split('-')[0] if '-' in user_lang else user_lang
        if lang_code in available_languages:
            return lang_code
    return settings.USERS_DEFAULT_LANGUAGE_CODE


@csrf_exempt
# @require_http_methods(["POST"])
def update_profile_settings(request, access_token):
    lang = get_preferred_language(request)    
    if request.method != "POST":
        return JsonResponse({"error":"invalid_method", "details": ft_i18n.get_translation(lang, "this_request_must_be_post")})
    try:
        user = User.objects.get(token=access_token)
    except Exception as e:
        return JsonResponse({"error":"user_not_found", "details":ft_i18n.get_translation(lang, "cannot_find_user_with_this_token")})
    if not user:
        return JsonResponse({"error":"user_not_found", "details":ft_i18n.get_translation(lang, "cannot_find_user_with_this_token")})

    userSettings = UserSettings.objects.get(user_id=user.user_id)

    display_name = request.POST.get("display_name")
    if display_name:
        userSettings.display_name = display_name

    github_url = request.POST.get("github_url")
    if github_url:
        userSettings.github = github_url
        
    status_message = request.POST.get("status_message")
    if status_message:
        userSettings.status_message = status_message

    lang = request.POST.get("lang")
    if lang:
        userSettings.lang = lang

    avatar = request.FILES.get("avatar")
    if avatar:
        max_size_mb = 2
        max_size_bytes = max_size_mb * 1024 * 1024
        if avatar.size > max_size_bytes:
            return JsonResponse({'error': 'invalid_file_size', "details":"file_size_exceeds_2mb"})

        allowed_extensions = ['jpg', 'jpeg', 'png']
        file_extension = avatar.name.split('.')[-1].lower()
        if file_extension not in allowed_extensions:
            return JsonResponse({'error': 'invalid_file_extension', "details":"only_jpg_and_png_are_allowed"})

        new_filename = f"user_{user.user_id}.{file_extension}"
        new_file_path = os.path.join(settings.MEDIA_ROOT, f'avatars', new_filename)
        path_name = f'/avatars/{new_filename}'


        with default_storage.open(new_file_path, 'wb+') as destination:
            for chunk in avatar.chunks():
                destination.write(chunk)

        userSettings.avatar.name = path_name

    userSettings.save()
    return JsonResponse({"success":"profile_settings_saved"})

@csrf_exempt
def update_confidentiality_settings(request, access_token):
    if request.method != "POST":
        return JsonResponse({"error":"invalid_method", "details":"this_request_must_be_post"})

    user = User.objects.get(token=access_token)
    if not user:
        return JsonResponse({"error":"user_not_found", "details":"cannot_find_user_with_this_token"})
    
    userConfidentiality = UserConfidentialitySettings.objects.get(user_id=user.user_id)
    
    profile_visibility = request.POST.get("profile_visibility")
    if profile_visibility:
        userConfidentiality.profile_visibility = profile_visibility
    
    show_fullname = request.POST.get("profile_show_fullname")
    if show_fullname:
        userConfidentiality.show_fullname = True if show_fullname == "on" else False
    else:
        userConfidentiality.show_fullname = False


    show_email = request.POST.get("profile_show_email")
    if show_email:
        userConfidentiality.show_email = True if show_email == "on" else False
    else:
        userConfidentiality.show_email = False

    userConfidentiality.save()

    return JsonResponse({ "success": "confidentiality_settings_saved" })

@csrf_exempt
def delete_account(request, access_token):
    if request.method != "DELETE":
        return JsonResponse({"error":"invalid_method", "details":"this_request_must_be_delete"})

    user = User.objects.get(token=access_token)
    if not user:
        return JsonResponse({"error":"user_not_found", "details":"cannot_find_user_with_this_token"})
    
    userSettings = UserSettings.objects.get(user_id=user.user_id)
    userConfidentialitySettings = UserConfidentialitySettings.objects.get(user_id=user.user_id)

    userSettings.delete()
    userConfidentialitySettings.delete()
    user.delete()
    return JsonResponse({"success": "account_successfully_deleted"})