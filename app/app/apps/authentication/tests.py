from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status 
from django.urls import reverse

class AuthenticationAPITestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com',
        }
        self.user_url = reverse('authentication:register-user')
        self.login_url = reverse('authentication:auth-login')
        self.user_retieve_update_url = reverse('authentication:user-retrieve-update')


    def test_create_user(self):
        response = self.client.post(self.user_url, {"user": self.user_data}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(),1)
        self.assertEqual(get_user_model().objects.first().username, self.user_data['username'])

    def test_login_user_with_user(self):
        get_user_model().objects.create_user(**self.user_data)

        response = self.client.post(self.login_url, {"user": self.user_data}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_user_without_user(self):
        response = self.client.post(self.login_url, {"user": self.user_data}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_with_auth(self):
        user = get_user_model().objects.create_user(**self.user_data)

        self.client.force_authenticate(user=user)
        response = self.client.get(self.user_retieve_update_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)

    def test_retrieve_user_without_auth(self):
        response = self.client.get(self.user_retieve_update_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user(self):
        user = get_user_model().objects.create_user(**self.user_data)

        self.client.force_authenticate(user=user)
        response = self.client.put(self.user_retieve_update_url, data={"user": {'username': 'testusernamechanged'}}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)
        self.assertEqual('testusernamechanged', response.data.get('username'))

    def test_list_user(self):
        user = get_user_model().objects.create_user(**self.user_data)
        url = reverse('authentication:user-list')

        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertEqual(get_user_model().objects.count(), response.data.get("count"))
