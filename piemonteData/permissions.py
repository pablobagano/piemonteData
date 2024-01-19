from rest_framework.permissions import BasePermission


class diretoriaPermissions(BasePermission):
    """
    Custom permission model for Directors
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        user_profile = getattr(request.user, 'userprofile', None)
        return user_profile and user_profile.diretoria_member()

class gerenciaPermissions(BasePermission):
    """
        Ensures that each manager only has access to the data of agentes subordinated to them
    """
    def has_object_permission(self, request, view, obj):
        
        if not request.user.is_authenticated:
            return False

        user_profile = getattr(request.user, 'userprofile', None)
        if not user_profile.gerencia_member():
            return False
        
        return request.user == obj.supervisor.gerencia.user