from users_service_app.models import *
from django.core.files.storage import default_storage
from django.conf import settings
from django.views.decorators.http import require_http_methods
import os
from django.conf import settings
from users_service_app.response_messages import error_response, success_response


@require_http_methods(["POST"])
def update_profile_settings(request, access_token):
    try:
        user = User.objects.get(token=access_token)
    except Exception as e:
        return error_response(request, "user_not_found", "cannot_find_user_with_this_token", status_code=404)
    if not user:
        return error_response(request, "user_not_found", "cannot_find_user_with_this_token", status_code=404)

    userSettings = UserSettings.objects.get(user_id=user.user_id)

    display_name = request.POST.get("display_name")
    if display_name:
        if len(display_name) > 20:
            return error_response(request, "field_too_long", "display_name_too_long")
        
        if UserSettings.objects.filter(display_name=display_name).exists():
            if not UserSettings.objects.filter(display_name=display_name).get().user_id == userSettings.user_id:
                return error_response(request, "invalid_displayname", "displayname_already_used")
        userSettings.display_name = display_name

    github_url = request.POST.get("github_url")
    if github_url:
        if len(github_url) > 39:
            return error_response(request, "field_too_long", "github_too_long")
        userSettings.github = github_url

    status_message = request.POST.get("status_message")
    if status_message:
        if len(status_message) > 80:
            return error_response(request, "field_too_long", "status_too_long")
        userSettings.status_message = status_message

    lang = request.POST.get("lang")
    if lang:
        userSettings.lang = lang

    avatar = request.FILES.get("avatar")
    if avatar:
        max_size_mb = 2
        max_size_bytes = max_size_mb * 1024 * 1024
        if avatar.size > max_size_bytes:
            return error_response(request, "invalid_file_size", "file_size_exceeds_2mb")

        allowed_extensions = ["jpg", "jpeg", "png"]
        file_extension = avatar.name.split(".")[-1].lower()
        if file_extension not in allowed_extensions:
            return error_response(request, "invalid_file_extension", "only_jpg_and_png_are_allowed")

        new_filename = f"user_{user.user_id}.{file_extension}"
        new_file_path = os.path.join(settings.MEDIA_ROOT, f"avatars", new_filename)
        path_name = f"/avatars/{new_filename}"

        with default_storage.open(new_file_path, "wb+") as destination:
            for chunk in avatar.chunks():
                destination.write(chunk)

        userSettings.avatar.name = path_name

    userSettings.save()
    return success_response(request, "profile_settings_saved", translate=False)


@require_http_methods(["POST"])
def update_confidentiality_settings(request, access_token):
    try:
        user = User.objects.get(token=access_token)
    except Exception as e:
        return error_response(request, "user_not_found", "cannot_find_user_with_this_token", status_code=404)
    if not user:
        return error_response(request, "user_not_found", "cannot_find_user_with_this_token", status_code=404)

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

    return success_response(request, "confidentiality_settings_saved")


@require_http_methods(["DELETE"])
def delete_account(request, access_token):
    try:
        user = User.objects.get(token=access_token)
    except Exception as e:
        return error_response(request, "user_not_found", "cannot_find_user_with_this_token", status_code=404)
    if not user:
        return error_response(request, "user_not_found", "cannot_find_user_with_this_token", status_code=404)

    userSettings = UserSettings.objects.get(user_id=user.user_id)
    userConfidentialitySettings = UserConfidentialitySettings.objects.get(
        user_id=user.user_id
    )

    userSettings.delete()
    userConfidentialitySettings.delete()
    user.delete()
    return success_response(request, "account_successfully_deleted")
