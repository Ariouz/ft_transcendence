from users_service_app.models import User
from django.http import JsonResponse


# /'users/'
def users(request):
    users_list = User.objects.all()
    users_list = list(users_list.values())
    context = {
        "users": users_list,
    }

    return JsonResponse(context)

