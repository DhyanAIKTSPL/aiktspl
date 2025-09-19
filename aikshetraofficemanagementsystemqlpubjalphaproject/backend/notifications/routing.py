"""
WebSocket routing for real-time notifications.
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notifications/(?P<user_id>\w+)/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/attendance/(?P<user_id>\w+)/$', consumers.AttendanceConsumer.as_asgi()),
    re_path(r'ws/tasks/(?P<user_id>\w+)/$', consumers.TaskConsumer.as_asgi()),
    re_path(r'ws/system/$', consumers.SystemConsumer.as_asgi()),
]
