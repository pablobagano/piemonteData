from rest_framework import serializers
from piemonteData.models import Agente, Diretoria, Gerencia, Supervisao, UserProfile
from .validators import *

class DiretoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diretoria
        fields = '__all__'
    
    def validate(self, data):
        if not nome_valido(data['nome']):
            raise serializers.ValidationError({'nome':'O nome deve conter apenas letras'})
        if not sobrenome_valido(data['sobrenome']):
            raise serializers.ValidationError({'O sobrenome':'O sobrenome deve conter apenas letras'})
        if not matricula_valida(data['matricula']):
            raise serializers.ValidationError({'nome':'A matrícula deve conter apenas dígitos'})
        return data
    
class GerenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gerencia
        fields = '__all__'

    def validate(self, data):
        if not nome_valido(data['nome']):
            raise serializers.ValidationError({'nome':'O nome deve conter apenas letras'})
        if not sobrenome_valido(data['sobrenome']):
            raise serializers.ValidationError({'O sobrenome':'O sobrenome deve conter apenas letras'})
        if not matricula_valida(data['matricula']):
            raise serializers.ValidationError({'nome':'A matrícula deve conter apenas dígitos'})
        
class SupervisaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisao
        fields = '__all__'
    
    def validate(self, data):
        if not nome_valido(data['nome']):
            raise serializers.ValidationError({'nome':'O nome deve conter apenas letras'})
        if not sobrenome_valido(data['sobrenome']):
            raise serializers.ValidationError({'O sobrenome':'O sobrenome deve conter apenas letras'})
        if not matricula_valida(data['matricula']):
            raise serializers.ValidationError({'nome':'A matrícula deve conter apenas dígitos'})

class AgenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agente
        fields = '__all__'
    
    def validate(self, data):
        if not nome_valido(data['nome']):
            raise serializers.ValidationError({'nome':'O nome deve conter apenas letras'})
        if not sobrenome_valido(data['sobrenome']):
            raise serializers.ValidationError({'O sobrenome':'O sobrenome deve conter apenas letras'})
        if not matricula_valida(data['matricula']):
            raise serializers.ValidationError({'nome':'A matrícula deve conter apenas dígitos'})

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