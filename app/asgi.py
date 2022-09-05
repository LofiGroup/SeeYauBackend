"""
ASGI config for src project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()
django_asgi_app = get_asgi_application()

from chat.routing import chat_websocket_urlpatterns
from chat.middleware import ChatRoomMiddleWare
from auth.middleware import TokenAuthMiddleWare

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleWare(
            URLRouter(
                chat_websocket_urlpatterns
            ))
    )
})

# ws://localhost:8000/ws/chat
