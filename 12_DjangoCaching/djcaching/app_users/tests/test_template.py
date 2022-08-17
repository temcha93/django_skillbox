from django.test import TestCase
from django.urls import reverse


class UsersTemplateTest(TestCase):

    def test_register_template(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/register.html')

    def test_login_template(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/login.html')