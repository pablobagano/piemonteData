from django.shortcuts import render
from rest_framework import viewsets, generics
from piemonteData.models import Diretoria, Gerencia, Supervisao, Agente, UserProfile
from .serializer import DiretoriaSerializer, GerenciaSerializer, SupervisaoSerializer, AgenteSerializer, UserPofileSerializer,AgentesPorSupervisorSerializer, AgentesPorCidadeSerializer

class DiretoriaViewSet(viewsets.ModelViewSet):
    """Displays all board members"""
    queryset = Diretoria.objects.all()
    serializer_class = DiretoriaSerializer

class GerenciaViewSet(viewsets.ModelViewSet):
    """Displays all employees at management level"""
    queryset = Gerencia.objects.all()
    serializer_class = GerenciaSerializer

class SupervisaoViewSet(viewsets.ModelViewSet):
    """Displays all supervisors"""
    queryset = Supervisao.objects.all()
    serializer_class = SupervisaoSerializer

class AgenteViewSet(viewsets.ModelViewSet):
    """Displays all agents"""
    queryset = Agente.objects.all()
    serializer_class = AgenteSerializer

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
    def get_queryset(self):
        queryset = Agente.objects.all()
        cidade = self.request.query_params.get('cidade', None)
        if cidade is not None:
            queryset = queryset.filter(cidade=cidade)
        return queryset
    serializer_class = AgentesPorCidadeSerializer