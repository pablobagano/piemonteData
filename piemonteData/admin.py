from django.contrib import admin
from .models import Diretoria, Gerencia, Supervisao, Agente

# Register your models here.

class Diretor(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'matricula', 'email')

admin.site.register(Diretoria, Diretor)

class Gerente(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'matricula', 'email', 'diretor')

admin.site.register(Gerencia, Gerente)

class Supervisor(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'matricula', 'email', 'diretor', 'gerente')

admin.site.register(Supervisao, Supervisor)

class Agente(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'matricula', 'email', 'diretor', 'gerente', 'supervisor')

admin.site.register(Agente, Agente)

