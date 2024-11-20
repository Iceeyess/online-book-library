from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
import json
from users.models import User


class UserTestCase(APITestCase):
    """CRUD User model testing"""
    def setUp(self) -> None:
        # user creation
        self.superuser_data = dict(username='iceeyes', password='1234', email='test@gmail.com', is_staff=True,
                                is_superuser=True)
        self.client = APIClient()
        self.superuser = User.objects.create_user(**self.superuser_data)
        # user authorization
        auth_url = reverse('users:token-obtain-pair')
        data = dict(email='test@gmail.com', password='1234')
        self.token = self.client.post(path=auth_url, data=data).data.get('access')
        self.headers = {
                    'Authorization': f'Token {self.token}'
                }

    def test_create_genre(self):
        """Testing for creation user"""
        path = reverse('users:user-list')
        data = dict(username='Vasily-Ali-Babaich', email='vasily@test.com', password='1234', city='St.Petersburg')
        response = self.client.post(path=path, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
