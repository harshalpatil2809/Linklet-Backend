
"""
ASGI config for backend project.
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

from django.core.asgi import get_asgi_application

# Initialize Django before importing routing/consumers.
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import backend.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(backend.routing.websocket_urlpatterns)
    ),
})
