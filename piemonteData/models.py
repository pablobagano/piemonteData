from django.db import models
from django.contrib.auth.models import User
from info import * 
from .utils import create_user_and_send_email


"""
This project is developed for Piemonte Group, a company in the financial business. 
The class Diretoria, Gerencia, Supervisao and Agentes represent different hierarchical levels. Respectively Directors, Managers, Supervisors and Agents. 
Each class has standard attribuites, such as nome(name), sobrenome(last name), matricula (ID) and email.
Each object will also become a user to the platform, in which each hierachical level will hold differente access priveleges. 
All the objects are vertically connected through ForeignKey relationships. This design's intention is to reflect the company's organizational structure

Special Features:
- Custom save methods for automated user creation and email notifications.
- Hierarchical data integrity ensured through Django's ORM.

This structure allows for a clear representation of the company's hierarchy and efficient user management within the platform.
"""


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
        if self.email_sent != criacao_usuario:
            self.email_sent = criacao_usuario
            self.__class__.objects.filter(pk = self.pk).update(email_sent=criacao_usuario)

class Gerencia(models.Model):
    diretoria = models.ForeignKey(Diretoria, on_delete= models.CASCADE)
    nome = models.CharField(max_length=20, null=False, blank=False)
    sobrenome = models.CharField(max_length=30, null= False, blank=False)
    matricula = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField()
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    def save(self, *args, **kwargs):
        super(Gerencia, self).save(*args, **kwargs)
        criacao_usuario = create_user_and_send_email(self.nome, self.sobrenome, self.email)
        self.email_sent = criacao_usuario
        if self.email_sent != criacao_usuario:
            self.email_sent = criacao_usuario
            self.__class__.objects.filter(pk = self.pk).update(email_sent=criacao_usuario)


class Supervisao(models.Model):
    diretoria = models.ForeignKey(Diretoria, on_delete= models.CASCADE)
    gerencia = models.ForeignKey(Gerencia, on_delete= models.CASCADE)
    nome = models.CharField(max_length=20, null=True, blank=False)
    sobrenome = models.CharField(max_length=30, null=True, blank=False)
    matricula = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField()
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    def save(self, *args, **kwargs):
        super(Supervisao, self).save(*args, **kwargs)
        criacao_usuario = create_user_and_send_email(self.nome, self.sobrenome, self.email)
        self.email_sent = criacao_usuario
        if self.email_sent != criacao_usuario:
            self.email_sent = criacao_usuario
            self.__class__.objects.filter(pk = self.pk).update(email_sent=criacao_usuario)

class Agente(models.Model):
    diretoria = models.ForeignKey(Diretoria, on_delete= models.CASCADE)
    gerencia = models.ForeignKey(Gerencia, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisao, on_delete=models.CASCADE)
    nome = models.CharField(max_length=30, null=False, blank=False)
    sobrenome = models.CharField(max_length=50, null=False, blank=False)
    matricula = models.CharField(max_length=30, null=False, blank=False)
    cidade = models.CharField(max_length=50, choices=lista_cidades, null=False, blank= False)
    email = models.EmailField()
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    def save(self, *args, **kwargs):
        super(Supervisao, self).save(*args, **kwargs)
        criacao_usuario = create_user_and_send_email(self.nome, self.sobrenome, self.email)
        self.email_sent = criacao_usuario
        if self.email_sent != criacao_usuario:
            self.email_sent = criacao_usuario
            self.__class__.objects.filter(pk = self.pk).update(email_sent=criacao_usuario)   



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    must_change_password = models.BooleanField(default=False)