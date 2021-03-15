from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'session', views.SessionViewSet)
router.register(r'player-admin', views.PlayerViewSet)
router.register(r'player', views.GetOrUpdatePlayerViewSet)
router.register(r'producer', views.ProducerViewSet)
router.register(r'broker', views.BrokerViewSet)

