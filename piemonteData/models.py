from collections.abc import Iterable
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import logging
import os
from info import * 
# Create your models here.



class Diretoria(models.Model):
    nome = models.CharField(max_length=20, null=False, blank=False)
    sobrenome = models.CharField(max_length=20, null=False, blank=False)
    matricula = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField()
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    def save(self, *args, **kwargs):
        super(Diretoria, self).save(*args, **kwargs)
        base_username = str(self.nome).lower()+'.'+str(self.sobrenome).lower()
        username = base_username
        num = 1
        while User.objects.filter(username = username).exists():
            username = f"{base_username}{num}"
            num +=1 
        user, created  = User.objects.get_or_create(username=username)
        if created:
            user.first_name = self.nome
            user.last_name = self.sobrenome
            user.email = self.email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            password_reset_url = reverse('password_reset_confirm', kwargs={'uidb64':uid, 'token':token})
            try:
                send_mail(
                'Defina a sua senha',
                f"Por favor defina a sua senha no link a seguir: {password_reset_url}",
                [user.email], 
                fail_silently = False
            )
                self.email_sent = True
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.error(f"Não foi possivel enviar email de confirmação: {e}")
                self.email_sent = False
                try:
                    send_mail(
                    'Inconsistência de cadastro',
                    f"Não foi possível cadastra a senha de {user.username}",
                    os.getenv('EMAIL_HOST_USER'),
                    [os.getenv('EMAIL_HOST_USER')]
                )
                except Exception as fallback_error:
                    logger.error(f"Erro ao enviar email de fallback: {fallback_error}")
            
            super(Diretoria, self).save(*args, **kwargs)

class Gerencia(models.Model):
    diretor = models.ForeignKey(Diretoria, on_delete= models.CASCADE)
    nome = models.CharField(max_length=20, null=False, blank=False)
    sobrenome = models.CharField(max_length=30, null= False, blank=False)
    email = models.EmailField()
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    def save(self, *args, **kwargs):
        super(Gerencia, self).save(*args, **kwargs)
        base_username = str(self.nome).lower()+'.'+str(self.sobrenome).lower()
        username = base_username
        num = 1
        while User.objects.filter(username= username).exists():
            username = f"{base_username}{num}"
            num +=1
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.first_name = self.nome
            user.last_name = self.sobrenome
            user.email = self.email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            password_reset_url = reverse('password_reset_confirm', kwargs={'uidb64':uid, 'token':token})
            try:
                send_mail(
                'Defina a sua senha',
                f"Por favor defina a sua senha no link a seguir: {password_reset_url}",
                [user.email], 
                fail_silently = False
            )
                self.email_sent = True
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.error(f"Não foi possivel enviar email de confirmação: {e}")
                self.email_sent = False
                try:
                    send_mail(
                    'Inconsistência de cadastro',
                    f"Não foi possível cadastra a senha de {user.username}",
                    os.getenv('EMAIL_HOST_USER'),
                    [os.getenv('EMAIL_HOST_USER')]
                )
                except Exception as fallback_error:
                    logger.error(f"Erro ao enviar email de fallback: {fallback_error}")
                
            super(Gerencia, self).save(*args, **kwargs)


class Supervisao(models.Model):
    diretoria = models.ForeignKey(Diretoria, on_delete= models.CASCADE)
    gerencia = models.ForeignKey(Gerencia, on_delete= models.CASCADE)
    nome = models.CharField(max_length=20, null=True, blank=False)
    sobrenome = models.CharField(max_length=30, null=True, blank=False)
    email = models.EmailField()
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    def save(self, *args, **kwargs):
        super(Supervisao, self).save(*args, **kwargs)
        base_username = str(self.nome) + '.' + str(self.sobrenome)
        username = base_username
        num = 1
        while User.objects.filter(username = username).exists():
            username = f"{base_username}{num}"
            num += 1
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.first_name = self.nome
            user.last_name = self.sobrenome
            user.email = self.email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            password_reset_url = reverse('password_reset_confirm', kwargs={'uidb64':uid, 'token': token})
            try:
                send_mail(
                    'Defina sua senha',
                    f'Por favor defina sua senha no link a seguir: {password_reset_url}',
                    os.getenv('EMAIL_HOST_USER'),
                    [user.email]

                )
                self.email_sent = True
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.error(f"Não foi possivel enviar email de confirmação: {e}")
                self.email_sent = False
                try:
                    send_mail(
                        'Inconsistência de cadastro',
                        f"Não foi possível cadastrar a senha de {user.username}",
                        os.getenv('EMAIL_HOST_USER'),
                        [os.getenv('EMAIL_HOST_USER')]
                    )
                except Exception as fallback_error:
                    logger.error(f"Erro ao enviar email de fallback: {fallback_error}")

class Agente(models.Model):
    diretoria = models.ForeignKey(Diretoria, on_delete= models.CASCADE)
    gerencia = models.ForeignKey(Gerencia, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisao, on_delete=models.CASCADE)
    nome = models.CharField(max_length=30, null=False, blank=False)
    sobrenome = models.CharField(max_length=50, null=False, blank=False)
    cidade = models.CharField(max_length=50, choices=lista_cidades, null=False, blank= False)
    email = models.EmailField()
    email_sent = models.BooleanField

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    def save(self, *args, **kwargs):
        super(Supervisao, self).save(*args, **kwargs)
        base_username = str(self.nome)+'.'+str(self.sobrenome)
        username = base_username
        num = 1
        while User.objects.filter(username=username).exists():
            username = f"{username}{num}"
            num +=1 
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.first_name = self.nome
            user.last_name = self.sobrenome
            user.email = self.email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            password_reset_url = reverse('password_reset_confirm', kwargs={'uidb64':uid, 'token': token })
            try:
                send_mail(
                    'Defina sua senha', 
                    f'Por favor defina sua senha no link a seguir: {password_reset_url}',
                    os.getenv('EMAIL_HOST_USER'),
                    [user.email]
                )
                self.email_sent = True
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.error(f"Não foi possível email de confirmação: {e}")
                self.email_sent = False
                try:
                    send_mail(
                        'Inconsistência de cadastro',
                        f"Não foi possível cadastrar a senha de {username}",
                        os.getenv('EMAIL_HOST_USER'),
                        [os.getenv('EMAIL_HOST_USER')]
                    )
                except Exception as fallback_error:
                    logger.error(f"Erro ao enviar email de fallback {fallback_error}")
            
        

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    must_change_password = models.BooleanField(default=False)