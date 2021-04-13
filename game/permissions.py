from rest_framework.permissions import BasePermission


class IsInSession(BasePermission):
	"""
	Находится ли указанный пользователь в сессии
	"""
	message = 'That is not your session'

	def has_object_permission(self, request, view, obj):
		return request.user.player.filter(user=request.user.id).exists()


class IsThePlayer(BasePermission):
	"""
	Является ли отправитель запроса указанным игроком
	"""

	def has_permission(self, request, view):
		return hasattr(request, 'player')
