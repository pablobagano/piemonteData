from django.db import models
from django.contrib.auth.models import User
from info import * 
from .utils import create_user_and_send_email
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
        criacao_usuario = create_user_and_send_email(self.nome, self.sobrenome, self.email)
        self.email_sent = criacao_usuario
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
        criacao_usuario = create_user_and_send_email(self.nome, self.sobrenome, self.email)
        self.email_sent = criacao_usuario
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
        criacao_usuario = create_user_and_send_email(self.nome, self.sobrenome, self.email)
        super(Supervisao, self).save(*args, **kwargs)

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
        criacao_usuario = create_user_and_send_email(self.nome, self.sobrenome, self.email)
        self.email_sent = criacao_usuario
        super(Supervisao, self).save(*args, **kwargs)    
        

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    must_change_password = models.BooleanField(default=False)