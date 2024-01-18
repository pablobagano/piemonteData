from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from piemonteData.models import Diretoria, UserProfile
from django.urls import reverse
from django.contrib.auth.models import User

class diretoriaTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('Diretoria-list')
        self.user = User.objects.create(username = 'testuser', password = 'test-password')
        UserProfile.objects.create(user=self.user, role='diretor')
        self.client.force_authenticate(user=self.user)
    
        self.diretor1 = Diretoria.objects.create(
            nome = 'José Cláudio',
            sobrenome =  'Ferreira Dias',
            matricula = 'JD123456',
        )
    
    def test_get_method_diretoria_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_method_diretoria(self):
        data = {
            'nome':'Reginaldo',
            'sobrenome' : 'Rossi',
            'matricula' : 'RR123456',
            'email' : 'adm@piemontecred.com.br'
        }
        response = self.client.post(self.list_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_delete_method_diretoria(self):
        response = self.client.delete('/diretoria/1/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_put_method_diretoria(self):
        data = {
            'nome':'Reginaldo',
            'sobrenome' : 'Faria',
            'matricula' : 'RF123456',
            'email' : 'adm@piemontecred.com.br'
        }
        response = self.client.put('/diretoria/1/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        