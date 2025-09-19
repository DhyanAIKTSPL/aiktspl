"""
ASGI config for office_management project.
Supports both HTTP and WebSocket protocols for real-time functionality.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'office_management.settings')

# Import WebSocket routing
from notifications.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    # HTTP protocol
    "http": get_asgi_application(),
    
    # WebSocket protocol for real-time features
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
