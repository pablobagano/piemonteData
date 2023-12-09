import django_filters
from .models import Agente

class AgenteFilter(django_filters.FilterSet):
    nome_supervisor = django_filters.CharFilter(field_name='supervisor__nome', lookup_expr='icontains')

    class Meta:
        model = Agente
        fields = ['email_sent', 'supervisor', 'nome_supervisor', 'cidade']