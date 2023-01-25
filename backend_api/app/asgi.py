"""
ASGI config for src project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.conf import settings
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django_asgi_app = get_asgi_application()

from app.websocket.routing import websocket_urlpatterns
from auth.middleware import TokenAuthMiddleWare

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleWare(
            URLRouter(
                websocket_urlpatterns
            ))
    )
})

import sys
from debug.init import init_debug
from utils.utils import entries_in_list
from firebase_admin import initialize_app

initialize_app()

if not entries_in_list(["makemigrations", "migrate", "collectstatic"], sys.argv[1:]) and not settings.IS_PRODUCTION_VERSION:
    print("Initializing debug version")
    init_debug()
