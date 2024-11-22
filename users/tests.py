from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
import json
from users.models import User


class UserTestCase(APITestCase):
    """CRUD User model testing"""
    def setUp(self) -> None:
        # user creation
        self.user_date = dict(username='iceeyes', password='1234', email='test@gmail.com', is_staff=True,
                              is_superuser=True)
        self.client = APIClient()
        self.user = User.objects.create_user(**self.user_date)
        # user authorization
        auth_url = reverse('users:token-obtain-pair')
        data = dict(email='test@gmail.com', password='1234')
        self.token = self.client.post(path=auth_url, data=data).data.get('access')
        self.headers = {
                    'Authorization': f'Token {self.token}'
                }

    def test_create_user(self):
        """Testing for creation user"""
        path = reverse('users:user-list')
        data = dict(username='Vasily-Ali-Babaich', email='vasily@test.com', password='1234', city='St.Petersburg')
        response = self.client.post(path=path, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user(self):
        """Testing for update user by one attribute called by City"""
        user = User.objects.all().last()
        path = reverse('users:user-detail', kwargs=dict(pk=user.id))
        data = dict(city='Moscow')
        response = self.client.patch(path=path, data=data, format='json', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get('city'), data.get('city'))

    def test_get_user(self):
        """Testing for getting user created in service method ->SetUp"""
        path = reverse('users:user-list')
        response = self.client.get(path=path, format='json', headers=self.headers)
        self.assertTrue(json.loads(response.content)[0].get('username'), 'iceeyes')

    def test_destroy_user(self):
        """Testing for deleting user created in service method -> SetUp"""
        path = reverse('users:user-detail', kwargs=dict(pk=User.objects.filter(username='iceeyes').last().id))
        response = self.client.delete(path=path, format='json', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)
