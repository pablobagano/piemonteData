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
    cargo = models.CharField(max_length=20, default='diretor')
    email = models.EmailField()
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    
    def save(self, *args, **kwargs):
        email_sent_before_save = self.email_sent
        super(Diretoria, self).save(*args, **kwargs)
        criacao_usuario, new_user = create_user_and_send_email(self.nome, self.sobrenome, self.cargo, self.email)
        new_user.root_id = self.id
        new_user.save()

        if criacao_usuario and not email_sent_before_save:
            self.email_sent = True
            super(Diretoria, self).save(update_fields=['email_sent'])

class Gerencia(models.Model):
    diretoria = models.ForeignKey(Diretoria, on_delete= models.SET_NULL, null=True)
    nome = models.CharField(max_length=20, null=False, blank=False)
    sobrenome = models.CharField(max_length=30, null= False, blank=False)
    matricula = models.CharField(max_length=30, null=False, blank=False)
    cargo = models.CharField(max_length=20, default='gerente')
    email = models.EmailField()
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    def save(self, *args, **kwargs):
        email_sent_before_save = self.email_sent
        super(Gerencia, self).save(*args, **kwargs)
        criacao_usuario, new_user = create_user_and_send_email(self.nome, self.sobrenome, self.cargo, self.email)
        new_user.root_id = self.id
        new_user.save()

        if criacao_usuario and not email_sent_before_save:
            self.email_sent = True
            super(Gerencia, self).save(update_fields=['email_sent'])


class Supervisao(models.Model):
    diretoria = models.ForeignKey(Diretoria, on_delete= models.SET_NULL, null=True)
    gerencia = models.ForeignKey(Gerencia, on_delete= models.SET_NULL, null=True)
    nome = models.CharField(max_length=20, null=True, blank=False)
    sobrenome = models.CharField(max_length=30, null=True, blank=False)
    matricula = models.CharField(max_length=30, null=False, blank=False)
    cargo = models.CharField(max_length=20, default='supervisor')
    email = models.EmailField()
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    def save(self, *args, **kwargs):
        email_sent_before_save = self.email_sent
        super(Supervisao, self).save(*args, **kwargs)
        criacao_usuario, new_user= create_user_and_send_email(self.nome, self.sobrenome, self.cargo, self.email)
        new_user.gerencia = self.gerencia
        new_user.root_id = self.id
        new_user.save()
        
        
        if criacao_usuario and not email_sent_before_save:
            self.email_sent = True
            super(Supervisao, self).save(update_fields=['email_sent'])

class Agente(models.Model):
    diretoria = models.ForeignKey(Diretoria, on_delete= models.SET_NULL, null=True)
    gerencia = models.ForeignKey(Gerencia, on_delete= models.SET_NULL, null=True)
    supervisor = models.ForeignKey(Supervisao, on_delete= models.SET_NULL, null=True)
    nome = models.CharField(max_length=30, null=False, blank=False)
    sobrenome = models.CharField(max_length=50, null=False, blank=False)
    matricula = models.CharField(max_length=30, null=False, blank=False)
    cargo = models.CharField(max_length=20, default='agente')
    cidade = models.CharField(max_length=50, choices=lista_cidades, null=False, blank= False)
    email = models.EmailField()
    email_sent = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    def save(self, *args, **kwargs):
        if self.supervisor and not self.gerencia:
            self.gerencia = self.supervisor.gerencia
        email_sent_before_save = self.email_sent
        super(Agente, self).save(*args, **kwargs)
        criacao_usuario, new_user = create_user_and_send_email(self.nome, self.sobrenome, self.cargo, self.email)
        new_user.gerencia = self.gerencia
        new_user.supervisor = self.supervisor
        new_user.root_id = self.id
        new_user.save()

        if criacao_usuario and not email_sent_before_save:
            self.email_sent = True
            super(Agente, self).save(update_fields=['email_sent'])   



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.PROTECT, null=False)
    nome = models.CharField(max_length=30, null=False, blank=False, default = None)
    sobrenome = models.CharField(max_length=30, null=False, blank=False, default = None)
    root_id = models.IntegerField(null=True, blank=False)
    role = models.CharField(max_length=15, null=False, blank=False, default=None)
    gerencia = models.ForeignKey(Gerencia, on_delete=models.SET_NULL, null=True, blank=True)
    supervisao = models.ForeignKey(Supervisao, on_delete=models.SET_NULL, null=True, blank=True)
    must_change_password = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def diretoria_member(self):
        return self.role == 'diretor'
    
    def gerencia_member(self):
        return self.role == 'gerente'
    
    def supervisao_member(self):
        return self.role == 'supervisor'
    
    def agente_member(self):
        return self.role == 'agente' 
    
   