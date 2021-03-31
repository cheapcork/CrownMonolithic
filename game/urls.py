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
	# path('/'),
	# path('map/'),
	# path('negotiation/'),
	# path('trade/'),
	path('join/<session_pk>/', views.join_session_view),
	path('count-turn/<pk>/', views.count_turn_view),
	path('leave/<session_pk>/', views.leave_session_view),

	# Template for testing ws
	path('test_ws', views.test_ws)
]
