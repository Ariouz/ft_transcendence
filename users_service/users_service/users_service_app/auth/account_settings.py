from users_service_app.models import *
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .ft_api import get_access_token, get_user_data
from uuid import uuid4
import os

@csrf_exempt
def update_profile_settings(request, access_token):
    if request.method != "POST":
        return JsonResponse({"error":"Invalid method", "details":"This request must be POST"})

    user = User.objects.get(token=access_token)
    if not user:
        return JsonResponse({"error":"User not found", "details":"Cannot find user with this token"})

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
            return JsonResponse({'error': 'Invalid file size', "details":"File size exceeds 2MB."})

        allowed_extensions = ['jpg', 'jpeg', 'png']
        file_extension = avatar.name.split('.')[-1].lower()
        if file_extension not in allowed_extensions:
            return JsonResponse({'error': 'Invalid file extension.', "details":"Only .jpg and .png are allowed."})

        new_filename = f"user_{user.user_id}.{file_extension}"
        new_file_path = os.path.join(settings.MEDIA_ROOT, f'avatars', new_filename)
        path_name = f'/avatars/{new_filename}'


        with default_storage.open(new_file_path, 'wb+') as destination:
            for chunk in avatar.chunks():
                destination.write(chunk)

        userSettings.avatar.name = path_name

    userSettings.save()
    return JsonResponse({"success":"Profile settings saved !"})

@csrf_exempt
def update_confidentiality_settings(request, access_token):
    if request.method != "POST":
        return JsonResponse({"error":"Invalid method", "details":"This request must be POST"})

    user = User.objects.get(token=access_token)
    if not user:
        return JsonResponse({"error":"User not found", "details":"Cannot find user with this token"})
    
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

    return JsonResponse({ "success": "Confidentiality settings saved!" })