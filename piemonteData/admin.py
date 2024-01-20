from django.contrib import admin
from .models import Diretoria, Gerencia, Supervisao, Agente, UserProfile

# Register your models here.

class DiretorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'matricula', 'email')
    list_display_links = ('id', 'nome', 'matricula')
    search_fields = ('nome', 'matricula',)
    list_per_page = 20

admin.site.register(Diretoria, DiretorAdmin)

class GerenteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'matricula', 'email', 'diretoria')  
    list_display_links = ('id', 'nome', 'matricula')
    search_fields = ('nome', 'matricula',)
    list_per_page = 20

admin.site.register(Gerencia, GerenteAdmin)

class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'matricula', 'email', 'diretoria', 'gerencia')
    list_display_links = ('id', 'nome', 'matricula')
    search_fields = ('nome', 'matricula',)
    list_per_page = 20

admin.site.register(Supervisao, SupervisorAdmin)

class AgenteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'matricula', 'cidade', 'email', 'diretoria', 'gerencia', 'supervisor')
    list_display_links = ('id', 'nome', 'matricula')
    search_fields = ('nome', 'matricula', 'supervisor','cidade',)
    list_per_page = 20

admin.site.register(Agente, AgenteAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nome', 'sobrenome', 'role', 'gerencia', 'supervisao')
    list_display_links = ('user','nome', 'sobrenome', 'role', 'gerencia', 'supervisao')
    search_field = ('user', 'role', 'gerencia', 'supervisao')
    list_per_page = 20

admin.site.register(UserProfile, UserProfileAdmin)


