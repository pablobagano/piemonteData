from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Diretoria(models.Model):
    nome = models.CharField(max_length=20, null=False, blank=False)
    sobrenome = models.CharField(max_length=20, null=False, blank=False)
    matricula = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    def save(self, *args, **kwargs):
        super(Diretoria, self).save(*args, **kwargs)
        username = str(self.nome).lower()+'.'+str(self.sobrenome).lower()
        user, created  = User.objects.get_or_create(username=username)
        if created:
            user.set_password(f"{self.nome}"+"1234")
            user.first_name = self.nome
            user.save()
            UserProfile.objects.create(user=user, must_change_password=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    must_change_password = models.BooleanField(default=False)