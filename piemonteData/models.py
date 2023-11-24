from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
# Create your models here.



class Diretoria(models.Model):
    nome = models.CharField(max_length=20, null=False, blank=False)
    sobrenome = models.CharField(max_length=20, null=False, blank=False)
    matricula = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    def save(self, *args, **kwargs):
        super(Diretoria, self).save(*args, **kwargs)
        username = str(self.nome).lower()+'.'+str(self.sobrenome).lower()
        user, created  = User.objects.get_or_create(username=username)
        if created:
            user.first_name = self.nome
            user.last_name = self.sobrenome
            user.is_superuser = True
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            password_reset_url = reverse('password_reset_confirm', kwargs={'uidb64':uid, 'token':token})
            send_mail(
                'Defina a sua senha',
                f"Por favor defina a sua senha no link a seguir: {password_reset_url}",
                [user.email], 
                fail_silently = False
            )



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    must_change_password = models.BooleanField(default=False)