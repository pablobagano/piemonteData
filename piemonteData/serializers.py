from rest_framework import serializers
from piemonteData.models import Agente, Diretoria, Gerencia, Supervisao, UserProfile
from .validators import *
from .utils import validate

class DiretoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diretoria
        fields = '__all__'
    
    def validate(self, data):
        return validate(data)
    
class GerenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gerencia
        fields = '__all__'

    def validate(self, data):
        return validate(data)
        
class SupervisaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisao
        fields = '__all__'
    
    def validate(self, data):
        return validate(data)

class AgenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agente
        fields = '__all__'

        def validate(self, data):
         return validate(data)
 
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
    
    def get_username(self,obj):
        return obj.user