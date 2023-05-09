import requests
from django.test import TestCase
from django.urls import reverse
from project.models import User


class CustomTest(TestCase):
    def test_user_creation(self):
        User.objects.create_user(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        self.assertTrue(user.check_password('test_password'))

    def test_auth(self):
        User.objects.create_user(username='test_user', password='test_password')
        data = {
            'username': 'test_user',
            'password': 'test_password'
        }
        response = self.client.post(reverse('user_auth'), data)
        self.assertEqual(response.status_code, 200)

    def test_using_header(self):
        User.objects.create_user(username='test_user', password='test_password')
        data = {
            'username': 'test_user',
            'password': 'test_password'
        }
        response = self.client.post(reverse('user_auth'), data)
        token = response.data.get('token')

        headers = {
            'Authorization': f'Bearer {token}',
        }

        response = self.client.post(reverse('test_auth'), data={}, headers=headers)
        self.assertEqual(response.data.get('text'), 123)

    def test_external_api(self):
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTQ4MzAwODgsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9lcmlrYXJzdGFteWFuIn0.qqTiGFIdLey4Kaa16_YQChpj5yzeZSONod0CTmlhmDw',
        }

        payload = {
            'id': 2,
            'phone': int('79008002343'),
            'text': 'test_message'
        }
        response = requests.post(url='https://probe.fbrq.cloud/v1/send/2', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)