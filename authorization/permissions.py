from rest_framework.permissions import BasePermission


class IsPlayer(BasePermission):
	"""
	Является ли игроком
	"""
	def has_permission(self, request, view):
		return hasattr(request, 'player')
