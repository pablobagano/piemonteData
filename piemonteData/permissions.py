from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class diretoriaPermissions(BasePermission):
    """
    Custom permission model for Directors
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        user_profile = getattr(request.user, 'userprofile', None)
        return user_profile and user_profile.diretoria_member()

class adminstrationPermissions(BasePermission):
     """
     Custom permissions for Managers
     """
     def has_permission(self, request, view):
        if not request.user.is_authenticated:
             return False
        user_profile = getattr(request.user, 'userprofile', None)
        if not user_profile:
             return False
        return user_profile.gerencia_member() or user_profile.diretoria_member()

def get_filtered_queryset_for_permissions(user, model, role_check, gerencia_field=None, supervisao_field=None):
    """
        This function grants specifics access level to each hiearchical level of the company
    """
    user_profile = getattr(user, 'userprofile', None)
    
    if not user_profile:
        raise PermissionDenied("Você não tem permissão para acessar estes dados")
    
    if role_check(user_profile):
            if user_profile.gerencia_member():
                 gerencia_field = user_profile.root_id
                 return model.objects.filter(gerencia=gerencia_field)
            elif user_profile.supervisao_member():
                 supervisao_field = user_profile.root_id
                 return model.objects.filter(supervisao=supervisao_field)
            elif user_profile.agente_member():
                 raise PermissionDenied("Seus níveis de acesso são insuficientes")
            else:
                return model.objects.all()
    else:
        raise PermissionDenied("Você não tem permissão para acessar esses dados")
