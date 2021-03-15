from django.urls import path, include
from django.contrib import admin
from .router import router

# Роуты для внутриигрового взаимодействия:
#  - Главный экран игры
#  - Подгрузка карты
#  - Подгрузка экрана для этапа переговоров
#  - Подгрузка окна сделки и отправка сделки производителем

urlpatterns = [
	# path('/'),
	# path('map/'),
	# path('negotiation/'),
	# path('trade/'),
]
