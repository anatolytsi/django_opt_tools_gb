import random
import string

from django.conf import settings
from django.test import TestCase, Client

from authapp.models import User


class TestUserAuthTestCase(TestCase):
    username = "django"
    email = "django@gb.local"
    password = 'geekbrains'

    def setUp(self):
        self.admin = User.objects.create_superuser(username=self.username, email=self.email, password=self.password)
        self.client = Client()

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, 'Пользователь')

        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertTrue(response.context['user'], self.admin)

        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertContains(response, 'Профиль')

    def test_basket_login_redirect(self):
        response = self.client.get('/auth/profile/')
        self.assertEqual(response.url, '/auth/login/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/auth/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['baskets']), [])

    def test_user_register(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)

        random_data = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))

        new_user_data = {
            'username': f'django{random_data}',
            'password1': self.password,
            'password2': self.password,
            'email': f'django{random_data}@ex.com',
            'age': 23
        }

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 302)

        new_user = User.objects.get(username=f'django{random_data}')

        activation_url = f'{settings.DOMAIN_NAME}/auth/verify/{new_user_data["email"]}/{new_user.activation_key}/'

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)
