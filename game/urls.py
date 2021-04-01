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
	path('count_turn/<pk>/', views.count_turn_view),
	path('leave/', views.leave_session_view),
	path('end_turn/', views.end_turn),
	path('cancel_end_turn/', views.cancel_end_turn),
	path('produce/', views.produce),
	path('is_started/<session_pk>/', views.is_started),

	# Template for testing ws
	path('test_ws', views.test_ws)
]
