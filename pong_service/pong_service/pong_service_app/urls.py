from django.urls import path
from .api import queue

urlpatterns = [
    path('queue/join/', queue.join_queue, name="join_queue"),
    path('queue/leave/', queue.leave_queue, name="leave_queue"),
]