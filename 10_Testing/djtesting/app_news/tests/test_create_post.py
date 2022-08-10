import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app_news.models import News

USERNAME = 'test'
USER_PASSWORD = 'xdrthnjil'


class TestCreatePost(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(username=USERNAME)
        user.set_password(USER_PASSWORD)
        user.save()

    def setUp(self):
        user = get_user_model().objects.get(username=USERNAME)
        self.client.force_login(user)

    def test_create_url_exists(self):
        url = reverse('create_news')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/new_news.html')

    def test_create_post_empty_form(self):
        url = reverse('create_news')
        form = {}
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(News.objects.count(), 0)

    def test_create_post_ok_form(self):
        url = reverse('create_news')
        form = {'title': 'Title_entry', 'description': 'Text of news.',
                'published_at': '2022-01-05'}
        response = self.client.post(url, form)
        url_next = reverse('edit_news',  args=[1])
        self.assertRedirects(response, url_next, status_code=302, target_status_code=200)
        self.assertEqual(News.objects.count(), 1)

    def test_create_post_form_one_pic(self):
        url = reverse('create_news')
        file_source = 'app_news/tests/data/test_pic1.jpg'
        with open(file_source, 'rb') as fp:
            form = {'title': 'Title_entry', 'description': 'Text of news.',
                    'published_at': '2022-01-05', 'file_field': [fp]}
            response = self.client.post(url, form)
        url_next = reverse('edit_news',  args=[1])
        self.assertRedirects(response, url_next, status_code=302, target_status_code=200)
        self.assertEqual(News.objects.count(), 1)
        news = News.objects.get(id=1)
        self.assertEqual(news.pictures.count(), 1)
        for pic in news.pictures.all():
            pic_to_del = pic.file
            if os.path.isfile(pic_to_del.path):
                os.remove(pic_to_del.path)
            # pic.delete()  # этот способ почему-то удаляет только ссылку в модели, но не файл на диске
        news.delete()

    def test_create_post_form_two_pic(self):
        url = reverse('create_news')
        file_source1 = 'app_news/tests/data/test_pic2.jpg'
        file_source2 = 'app_news/tests/data/test_pic3.jpg'
        with open(file_source1, 'rb') as fp1, open(file_source2, 'rb') as fp2:
            form = {'title': 'Title_entry', 'description': 'Text of news.',
                    'published_at': '2022-01-05', 'file_field': [fp1, fp2]}
            response = self.client.post(url, form)
        url_next = reverse('edit_news',  args=[1])
        self.assertRedirects(response, url_next, status_code=302, target_status_code=200)
        self.assertEqual(News.objects.count(), 1)
        news = News.objects.get(id=1)
        self.assertEqual(news.pictures.count(), 2)
        for pic in news.pictures.all():
            pic_to_del = pic.file
            if os.path.isfile(pic_to_del.path):
                os.remove(pic_to_del.path)
        news.delete()


class TestCreatePostWithoutAuth(TestCase):
    def test_create_get_not_allowed_without_auth(self):
        url = reverse('create_news')
        response = self.client.get(url)
        url_login = reverse('login')[:-1]
        url_next = f'{url_login}?next={url}'
        self.assertRedirects(response, url_next, status_code=302, target_status_code=301)

    def test_create_post_not_allowed_without_auth(self):
        url = reverse('create_news')
        form = {'title': 'Title_entry', 'description': 'Text of news.',
                'published_at': '2022-01-05'}
        response = self.client.post(url, form)
        url_login = reverse('login')[:-1]
        url_next = f'{url_login}?next={url}'
        self.assertRedirects(response, url_next, status_code=302, target_status_code=301)
