from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from pong_service_app.models import *
import ft_requests
import json
import logging
from .. import pong_user