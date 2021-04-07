from django.urls import path, include
from django.contrib import admin
from .router import router
from . import views

# Роуты для внутриигрового взаимодействия:
#  - Главный экран игры
#  - Подгрузка карты
#  - Подгрузка экрана для этапа переговоров
#  - Подгрузка окна сделки и отправка сделки производителем

urlpatterns = [
	path('lobby/join/<pk>/', ),
	path('lobby/leave/', ),
	path('lobby/detail/', )
]
