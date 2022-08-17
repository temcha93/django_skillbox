from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse
from app_users.models import User


USER = {
    'username': 'TestUser',
    'first_name': 'Bobbi',
    'last_name': 'Braun',
    'city': 'Moscow',
    'password1': 'Sc6-XU2-DTQ-Ae6',
    'password2': 'Sc6-XU2-DTQ-Ae6',
}


class UsersViewsTest(TestCase):

    def test_user_register(self):
        url = reverse('register')
        response = self.client.post(url, USER)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(str(User.objects.first()), 'TestUser')

        username = USER['username']
        password = USER['password1']
        self.assertTrue(authenticate(username=username, password=password))

        url = reverse('login')
        response = self.client.post(url, username=USER['username'], password=USER['password1'], follow=True)
        self.assertTrue(response.context['user'].is_active)