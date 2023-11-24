from django.shortcuts import render, HttpResponse
from django.core.mail import send_mail
from setup.settings import EMAIL_HOST_USER as user
import os

# Create your views here.

def test_email(request):
    try:
        send_mail(
            'Email Teste/Test Email',
            'Email Teste da PiemonteData/ This a test email from PiemonteData',
            os.getenv(user),
            [user, os.getenv('DIRETORIA'), os.getenv('GERENCIA')],
            fail_silently=False
        )
        return HttpResponse("Email enviado com sucesso/Email sent successfully!")
    except Exception as e:
        return HttpResponse(f"Falha no envio/ Email failed to send: {e}")
