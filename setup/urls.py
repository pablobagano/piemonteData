"""setup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import PasswordResetConfirmView
from piemonteData.views import DiretoriaViewSet, GerenciaViewSet, SupervisaoViewSet, AgenteViewSet, UserProfileViewSet, AgentesPorSupervisor, AgentesPorCidade
from rest_framework import routers 

router = routers.DefaultRouter()
router.register('diretoria', DiretoriaViewSet, basename='Diretoria')
router.register('gerencia', GerenciaViewSet, basename='Gerencia')
router.register('supervisores', SupervisaoViewSet, basename='Supervisao')
router.register('agentes', AgenteViewSet, basename='Agentes')
router.register('usuarios', UserProfileViewSet, basename= 'Usuarios')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls') ),
    path('', include(router.urls)),
    path('supervisores/<int:pk>/agentes/', AgentesPorSupervisor.as_view()),
    path('agentes/cidade', AgentesPorCidade.as_view())
] 
