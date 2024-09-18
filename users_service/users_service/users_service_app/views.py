from users_service_app.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


# /'users/'
@require_http_methods(["GET"])
def users(request):
    users_list = User.objects.all()
    users_list = list(users_list.values())
    context = {
        "users": users_list,
    }

    return JsonResponse(context)