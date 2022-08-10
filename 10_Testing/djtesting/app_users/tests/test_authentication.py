from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

USERNAME = 'test2'
USER_PASSWORD = 'xdrthnjil'
OLD_PASSWORD = 'testpassword'


class TestAuthentication(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(username=USERNAME)
        user.set_password(USER_PASSWORD)
        user.save()

    def test_authentication_url_exists(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_authentication_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'app_users/login.html')

    def test_authentication_register_correct(self):
        response = self.client.post(reverse('login'), {'username': USERNAME,
                                                        'password': USER_PASSWORD})
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)
        self.assertEqual(response.client.session.get('_auth_user_id'), '1')  # залогиненность

    def test_authentication_not_register_bad_data(self):
        response = self.client.post(reverse('login'), {'username': USERNAME,
                                                        'password': OLD_PASSWORD})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.client.session.get('_auth_user_id'), None)

    def test_logout_url_exists(self):
        user = get_user_model().objects.get(username=USERNAME)
        self.client.force_login(user)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)
        self.assertEqual(response.client.session.get('_auth_user_id'), None)

