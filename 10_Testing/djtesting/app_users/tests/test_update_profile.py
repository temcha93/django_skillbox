import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from app_users.models import Profile

USERNAME = 'test3'
USER_PASSWORD = 'xdrthnjil'
USER2 = 'test4'


class TestUpdateProfile(TestCase):
    @classmethod
#    def setUpClass(cls):
#        super(TestUpdateProfile, cls).setUpClass()
    def setUpTestData(cls):
        user = get_user_model().objects.create(username=USERNAME)
        user.set_password(USER_PASSWORD)
        user.save()
        profile = Profile.objects.create(user=user)
        profile.save()
        user = get_user_model().objects.create(username=USER2)
        user.set_password(USER_PASSWORD)
        user.save()
        profile = Profile.objects.create(user=user)
        profile.save()

    # def setUp(self):
    #    print("2?", get_user_model().objects.count())

    def test_update_url_exists(self):
        user = get_user_model().objects.get(username=USERNAME)
        self.client.force_login(user)
        url = reverse('edit_profile', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/update_profile.html')

    def test_update_url_only_users(self):
        user = get_user_model().objects.get(username=USER2)
        self.client.force_login(user)
        url_wrong = reverse('edit_profile', args=[1])
        url_right = reverse('edit_profile', args=[2])
        response = self.client.get(url_wrong)  # урл для редактирования чужого профиля
        self.assertRedirects(response, url_right, status_code=302, target_status_code=200)

    def test_update_not_allow_for_unauthenthicated(self):
        url = reverse('edit_profile', args=[1])
        response = self.client.get(url)
        url_login = reverse('login')[:-1]
        url_next = f'{url_login}?next={url}'
        self.assertRedirects(response, url_next, status_code=302, target_status_code=301)

    def test_update_data(self):
        user = get_user_model().objects.get(username=USERNAME)
        self.client.force_login(user)
        url = reverse('edit_profile', args=[1])
        form_data = {'name': 'Кто-то', 'last_name': 'Кокойтович',
                     'about': 'Не самый общительный в мире персонаж'}
        response = self.client.post(url, form_data)
        url_ok = reverse('account', args=[1])
        self.assertRedirects(response, url_ok, status_code=302, target_status_code=200)
        profile = user.profile
        self.assertEqual(profile.name, 'Кто-то')
        self.assertEqual(profile.last_name, 'Кокойтович')
        self.assertEqual(profile.about, 'Не самый общительный в мире персонаж')

    def test_update_data_with_wong_url(self):
        user = get_user_model().objects.get(username=USER2)
        self.client.force_login(user)
        url = reverse('edit_profile', args=[1])
        form_data = {'name': 'Некто',
                     'about': 'Упорно пытающийся отредактировать чужой профиль'}
        response = self.client.post(url, form_data)
        url_ok = reverse('edit_profile', args=[2])
        self.assertRedirects(response, url_ok, status_code=302, target_status_code=200)
        user1 = get_user_model().objects.get(username=USERNAME)
        profile = user1.profile
        self.assertEqual(profile.name, '')

    def test_update_data_with_avatar(self):
        user = get_user_model().objects.get(username=USERNAME)
        self.client.force_login(user)
        url = reverse('edit_profile', args=[1])
        url_ok = reverse('account', args=[1])
        file_source = 'app_users/tests/pics/test_avatar.png'
        file_destination = f'avatars/{USERNAME}_test_avatar.png'
        with open(file_source, 'rb') as fp:
            form_data = {'avatar': fp}
            response = self.client.post(url, form_data)
            self.assertRedirects(response, url_ok, status_code=302, target_status_code=200)
        user.refresh_from_db()
        self.assertEqual(user.profile.avatar, file_destination)
        response = self.client.post(url_ok)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, file_destination)

        with open(file_source, 'rb') as fp:  # редактирование по второму разу - ссылка на файл должна остаться той же
            form_data = {'avatar': fp}
            response = self.client.post(url, form_data)
            self.assertRedirects(response, url_ok, status_code=302, target_status_code=200)
        user.refresh_from_db()
        self.assertEqual(user.profile.avatar, file_destination)

        user.profile.avatar.delete()  # удалить картинку с диска, чтоб после тестирования не осталось мусора

    def test_update_data_with_clear_avatar(self):
        user = get_user_model().objects.get(username=USERNAME)
        self.client.force_login(user)
        url = reverse('edit_profile', args=[1])
        url_ok = reverse('account', args=[1])
        file_source = 'app_users/tests/pics/test_avatar.png'
        with open(file_source, 'rb') as fp:
            form_data = {'avatar': fp}
            response = self.client.post(url, form_data)
            self.assertRedirects(response, url_ok, status_code=302, target_status_code=200)
        user.refresh_from_db()
        file_avatar = user.profile.avatar

        form_data = {'avatar-clear': 1}
        response = self.client.post(url, form_data)
        self.assertRedirects(response, url_ok, status_code=302, target_status_code=200)
        user.refresh_from_db()
        self.assertFalse(bool(user.profile.avatar))

        self.assertFalse(os.path.isfile(file_avatar.path))  # при очищении аватары файл должен был удалиться

