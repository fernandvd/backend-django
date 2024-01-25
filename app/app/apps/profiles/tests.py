from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse 

from .models import Profile

class ProfileAPITestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='testuser@example.com', password='password')

        self.url_name_profile_detail = 'profiles:profile-detail'
        self.url_name_profile_follow = 'profiles:profile-follow'


    def test_retrieve_profile(self):
        url = reverse(self.url_name_profile_detail, kwargs={'username': self.user.username})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_profile(self):
        user = get_user_model().objects.create_user(username='testuser1', email='testuser1@example.com', password='password')
        url = reverse(self.url_name_profile_follow, kwargs={'username': self.user.username})

        self.client.force_authenticate(user=user)
        response = self.client.post(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)

    def test_unfollow_profile(self):
        user = get_user_model().objects.create_user(username='testuser1', email='testuser1@example.com', password='password')
        user1 = get_user_model().objects.create_user(username='testuser2', email='testuser2@example.com', password='password')

        url = reverse(self.url_name_profile_follow, kwargs={'username': self.user.username})
        self.client.force_authenticate(user=user)
        self.client.post(url, {}, format='json') #follow user

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
