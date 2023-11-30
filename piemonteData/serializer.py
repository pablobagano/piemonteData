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
        model = Supervisao
        fields = '__all__'

class UserPofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
