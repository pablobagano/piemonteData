from django.shortcuts import render
from rest_framework import viewsets, generics, filters
from piemonteData.models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AgenteFilter
from .permissions import diretoriaPermissions, get_filtered_queryset_for_permissions, adminstrationPermissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import BasicAuthentication

class DiretoriaViewSet(viewsets.ModelViewSet):
    """Displays all board members"""
    queryset = Diretoria.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, diretoriaPermissions]
    serializer_class = DiretoriaSerializer
    http_method_names = ['get', 'post', 'put', 'patch']
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['nome']
    search_fields = ['nome', 'matricula']
    filterset_fields = ['email_sent']

class GerenciaViewSet(viewsets.ModelViewSet):
    """Displays all employees at management level"""
    queryset = Gerencia.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, diretoriaPermissions]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    serializer_class = GerenciaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['nome']
    search_fields = ['nome', 'matricula']
    filterset_fields = ['email_sent']


class SupervisaoViewSet(viewsets.ModelViewSet):
    """Displays supervisor to their respective managers. Directors have unrestricted access"""
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    serializer_class = SupervisaoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['nome']
    search_fields = ['nome', 'matricula']
    filterset_fields = ['email_sent']

    def get_queryset(self):
        return get_filtered_queryset_for_permissions(
            user = self.request.user,
            model= Supervisao,
            role_check= lambda profile: profile.diretoria_member() or profile.gerencia_member() or profile.gerencia_member() or profile.agente_member()
        )

class AgenteViewSet(viewsets.ModelViewSet):
    """Displays agents to their respective managers and supervisors. Directors have unrestricted accesss"""
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    serializer_class = AgenteSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['nome']
    search_fields = ['nome', 'matricula', 'cidade']
    filterset_fields = ['email_sent', 'cidade']
    filterset_class = AgenteFilter

    def get_queryset(self):
        return get_filtered_queryset_for_permissions(
            user = self.request.user,
            model= Agente,
            role_check= lambda profile: profile.diretoria_member() or profile.gerencia_member() or profile.gerencia_member() or profile.agente_member()
        )

class UserProfileViewSet(viewsets.ModelViewSet):
    """Displays user profiles to the administrator"""
    queryset = UserProfile.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = UserPofileSerializer


class AgentesPorSupervisor(generics.ListAPIView):
    """Displays a list of agents per supervisor. Administration permissions (Managers or Directors) are required"""
    authentication_classes = [BasicAuthentication]
    permission_classes = [adminstrationPermissions]
    serializer_class = AgentesPorSupervisorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['nome']
    filterset_fields = ['supervisor']
    def get_queryset(self):
        queryset = Agente.objects.filter(supervisor_id = self.kwargs['pk'])
        return queryset
    

class AgentesPorCidade(generics.ListAPIView):
    """Displays a list of agents per city. Administration permissions (Managers or Directors) are required"""
    authentication_classes = [BasicAuthentication]
    permission_classes = [adminstrationPermissions]
    serializer_class = AgentesPorCidadeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['nome']
    filterset_fields = ['cidade']
    def get_queryset(self):
        queryset = Agente.objects.all()
        cidade = self.request.query_params.get('cidade', None)
        if cidade is not None:
            queryset = queryset.filter(cidade=cidade)
        return queryset
    