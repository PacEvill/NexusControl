import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import sensors.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensorview.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            sensors.routing.websocket_urlpatterns
        )
    ),
})
