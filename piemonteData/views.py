from django.shortcuts import render
from rest_framework import viewsets, generics, filters
from piemonteData.models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AgenteFilter

class DiretoriaViewSet(viewsets.ModelViewSet):
    """Displays all board members"""
    queryset = Diretoria.objects.all()
    serializer_class = DiretoriaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['nome']
    search_fields = ['nome', 'matricula']
    filterset_fields = ['email_sent']

class GerenciaViewSet(viewsets.ModelViewSet):
    """Displays all employees at management level"""
    queryset = Gerencia.objects.all()
    serializer_class = GerenciaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['nome']
    search_fields = ['nome', 'matricula']
    filterset_fields = ['email_sent']

class SupervisaoViewSet(viewsets.ModelViewSet):
    """Displays all supervisors"""
    queryset = Supervisao.objects.all()
    serializer_class = SupervisaoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['nome']
    search_fields = ['nome', 'matricula']
    filterset_fields = ['email_sent']

class AgenteViewSet(viewsets.ModelViewSet):
    """Displays all agents"""
    queryset = Agente.objects.all()
    serializer_class = AgenteSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['nome']
    search_fields = ['nome', 'matricula', 'cidade']
    filterset_fields = ['email_sent', 'cidade']
    filterset_class = AgenteFilter

class UserProfileViewSet(viewsets.ModelViewSet):
    """Displays user profiles"""
    queryset = UserProfile.objects.all()
    serializer_class = UserPofileSerializer

class AgentesPorSupervisor(generics.ListAPIView):
    """Displays a list of agents per supervisor"""
    def get_queryset(self):
        queryset = Agente.objects.filter(supervisor_id = self.kwargs['pk'])
        return queryset
    serializer_class = AgentesPorSupervisorSerializer

class AgentesPorCidade(generics.ListAPIView):
    """Displays a list of agents per city"""    
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
    