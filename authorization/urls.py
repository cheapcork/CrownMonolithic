from django.urls import path, include
from .views import create_player, me
# from .router import router

urlpatterns = [
    path('game/lobby/<pk>/join/', create_player),
    path('auth/me/', me),
    # path('/', include(router.urls))
]