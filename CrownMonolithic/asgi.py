"""
ASGI config for CrownMonolithic project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from game.middleware import TokenAuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import game.router

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CrownMonolithic.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddlewareStack(
        URLRouter(
            game.router.websocket_urlpatterns
        )
    ),
})
