from django.contrib.auth.models import User
from django.apps import apps
from django.core.mail import send_mail
import logging
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import os
from rest_framework import serializers
from .validators import * 
from django.conf import settings
from unidecode import unidecode

def create_user_and_send_email(first_name, last_name, cargo, email):
    """
    The function create_user_and_send_email automates the process of user creation when a now object representing an employee is created. 
    A username is created along with a link that is sent to the new employee's e-mail in which they will be request to reset their password.
    Aside form logging, the built-in Python library used to aid in exception handliing, all the procedures are executed Django's built-in functions
    """
    UserProfile = apps.get_model('piemonteData', 'UserProfile')
    first_name_part = unidecode(first_name.split()[0]) 
    last_name_part = unidecode(last_name.split()[-1]) 
    username = f"{first_name_part}.{last_name_part}".lower()
    num = 1
    while User.objects.filter(username= username).exists():
        username = f"{username}{num}"
        num += 1
    user, created = User.objects.get_or_create(username=username, defaults={
        'first_name': first_name,
        'last_name' : last_name, 
        'email' : email
    }) 
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    password_reset_url =  settings.BASE_URL + reverse('password_reset_confirm', kwargs= {
        'uidb64':uid, 
        'token': token
    })
    if created:
        new_user = UserProfile.objects.create(user=user, nome = first_name, sobrenome = last_name, role=cargo, must_change_password=True)
        try:
            send_mail(
                'Defina sua senha - PiemoneteData',
                f"Por defina a sua senha no link a seguir: {password_reset_url}",
                os.getenv('EMAIL_HOST_USER'),
                [user.email],
                fail_silently=False
            )
            return True, new_user
        except Exception:
            logger = logging.getLogger(__name__)
            logger.exception(f"Não foi possível enviar email de confirmação")
            try:
                send_mail(
                    'Inconsistência de cadastro',
                    f"Não foi possível cadastra a senha de {user.username}",
                    os.getenv('EMAIL_HOST_USER'),
                    [os.getenv('EMAIL_HOST_USER')]
                )
            except Exception:
                logger.exception(f"Erro ao enviar email de fallback")
            return False



# Validation Function 

def validate(data):
        if not nome_valido(data['nome']):
            raise serializers.ValidationError({'nome':'O nome deve conter apenas letras'})
        if not sobrenome_valido(data['sobrenome']):
            raise serializers.ValidationError({'sobrenome':'O sobrenome deve conter apenas letras'})
        if not matricula_valida(data['matricula']):
            raise serializers.ValidationError({'matricula':'A matrícula deve conter apenas dígitos'})
        return data