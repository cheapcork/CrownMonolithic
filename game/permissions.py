from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsInSessionOrAdmin(BasePermission):
    message = 'That is not your session'

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.player.filter(user=request.user.id).exists()