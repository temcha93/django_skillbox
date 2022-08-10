from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase
from django.urls import reverse


class TestRegistration(TestCase):
    def test_register_url_exists(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'app_users/register.html')

    def test_post_register_correct(self):
        response = self.client.post(reverse('register'), {'username': 'test1',
                                                          'password1': 'xdrthnjil',
                                                          'password2': 'xdrthnjil'})
        count_after = get_user_model().objects.count()
        self.assertEqual(count_after, 1)  # в базе появился один пользователь
        user = authenticate(username='test1', password='xdrthnjil')
        self.assertNotEqual(user, None)  # залогиниться этим пользователем можно
        self.assertRedirects(response, reverse('account', args=[user.pk]),
                             status_code=302, target_status_code=200)  # все успешно и редирект куда надо

    def test_post_register_not_correct(self):  # невалидная форма - только один из паролей заполнен
        response = self.client.post(reverse('register'), {'username': 'test1',
                                                          'password1': 'xdrthnjil'})
        self.assertEqual(response.status_code, 200)  # та же страница с формой
        self.assertFormError(response, 'form', 'password2', 'This field is required.')
        count_after = get_user_model().objects.count()
        self.assertEqual(count_after, 0)
