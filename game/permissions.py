from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsInSession(BasePermission):
	"""
	Находится ли указанный пользователь в сессии
	"""
	message = 'That is not your session'

	def has_object_permission(self, request, view, obj):
		return request.user.player.filter(user=request.user.id).exists()


class IsThePlayer(BasePermission):
	"""
	Является ли отправитель запроса игроком (для фильтрации запросов к другим игрокам)
	"""

	def has_object_permission(self, request, view, obj):
		pass


class SessionIsStarted(BasePermission):
	"""
	Проверяет, начата ли сессия
	"""
	def has_object_permission(self, request, view, obj):
		pass
