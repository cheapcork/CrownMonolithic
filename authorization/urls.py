from django.urls import path, include
from .views import create_player, me

urlpatterns = [
    path('create/', create_player),
    path('me/', me),
]