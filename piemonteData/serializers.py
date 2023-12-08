from rest_framework import serializers
from piemonteData.models import Agente, Diretoria, Gerencia, Supervisao, UserProfile

class DiretoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diretoria
        fields = '__all__'

class GerenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gerencia
        fields = '__all__'

class SupervisaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisao
        fields = '__all__'

class AgenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agente
        fields = '__all__'

class AgentesPorSupervisorSerializer(serializers.ModelSerializer):
    supervisor = serializers.ReadOnlyField(source='supervisor.nome')
    cidade = serializers.SerializerMethodField()
    class Meta:
        model = Agente
        fields = ['nome', 'sobrenome', 'cidade', 'matricula', 'supervisor']
    def get_cidade(self, obj):
        return obj.get_cidade_display()

class AgentesPorCidadeSerializer(serializers.ModelSerializer):
    cidade = serializers.SerializerMethodField()

    class Meta:
        model = Agente
        fields = ['nome', 'sobrenome', 'matricula', 'cidade']
    
    def get_cidade(self, obj):
        return obj.get_cidade_display()

class UserPofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'