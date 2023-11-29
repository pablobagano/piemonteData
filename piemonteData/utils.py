from django.contrib.auth.models import User
from django.core.mail import send_mail
import logging
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import logging
import os

def create_user_and_send_email(first_name, last_name, email):
    username = f"{first_name}.{last_name}".lower()
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
    password_reset_url = reverse('password_reset_confirm', kwargs= {
        'uidb64':uid, 
        'token': token
    })
    if created:
        try:
            send_mail(
                'Defina sua senha - PiemoneteData',
                f"Por defina a sua senha no link a seguir: {password_reset_url}",
                os.getenv('EMAIL_HOST_USER'),
                [user.mail],
                fail_silently=False
            )
            return True
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Não foi possível enviar email de confirmação: {e}")
            try:
                send_mail(
                    'Inconsistência de cadastro',
                    f"Não foi possível cadastra a senha de {user.username}",
                    os.getenv('EMAIL_HOST_USER'),
                    [os.getenv('EMAIL_HOST_USER')]
                )
            except Exception as fallback_error:
                logger.error(f"Erro ao enviar email de fallback: {fallback_error}")
            return False


