from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from piemonteData.models import Diretoria, UserProfile
from django.urls import reverse
from django.contrib.auth.models import User

class diretoriaTestCase(APITestCase):
    """
        Set up the test environment before running each test case.
        This includes creating a test client, a test user with a user profile,
        and a sample Diretoria instance for testing.
    """
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
        """
            Test the GET method for retrieving the list of diretoria.
            This test checks if the request is successful and returns HTTP 200 OK.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_method_diretoria(self):
        """
            Test the POST method for creating a new diretoria.
            This test submits a diretoria object and checks if it is created successfully
            with HTTP 201 Created response.
        """
        data = {
            'nome':'Reginaldo',
            'sobrenome' : 'Rossi',
            'matricula' : 'RR123456',
            'email' : 'adm@piemontecred.com.br'
        }
        response = self.client.post(self.list_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_delete_method_diretoria(self):
        """
            Test the DELETE method for a diretoria.
            This test attempts to delete a diretoria instance and checks if the method
            is not allowed (HTTP 405 Method Not Allowed), indicating delete operation
            is not supported for diretoria.
        """
        response = self.client.delete('/diretoria/1/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_put_method_diretoria(self):
        """
            Test the PUT method for updating a diretoria.
            This test updates a diretoria object and checks if the update is successful
            with HTTP 200 OK response.
        """
        data = {
            'nome':'Reginaldo',
            'sobrenome' : 'Faria',
            'matricula' : 'RF123456',
            'email' : 'adm@piemontecred.com.br'
        }
        response = self.client.put('/diretoria/1/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        