from rest_framework.routers import DefaultRouter
from . import views
from django.urls import re_path
from . import consumers

# from channels.routing import route
# from game.consumers import ws_connect, ws_disconnect


router = DefaultRouter()
router.register(r'session-admin', views.SessionLobbyViewSet)
router.register(r'session', views.SessionGameViewSet)
router.register(r'player-admin', views.PlayerListViewSet)
router.register(r'player', views.PlayerViewSet)
# router.register(r'player', views.GetOrUpdatePlayerViewSet)
# router.register(r'producer', views.ProducerViewSet)
# router.register(r'broker', views.BrokerViewSet)
router.register(r'transactions', views.TransactionViewSet)


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

