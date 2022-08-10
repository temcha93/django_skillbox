import os

from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import TestCase
from django.urls import reverse

from app_news.models import News, FileBlogPicture

USERNAME = 'test'
USER_PASSWORD = 'xdrthnjil'


class TestEditPost(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(username=USERNAME)
        user.set_password(USER_PASSWORD)
        user.save()
        News.objects.create(title='Title_entry', description='Text of news.',
                            published_at='2022-01-05', author=user, fl_ready_to_publish=False)

    def setUp(self):
        user = get_user_model().objects.get(username=USERNAME)
        self.client.force_login(user)

    def test_edit_url_exists(self):
        url = reverse('edit_news', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/new_news.html')

    def test_edit_post_form_plus_two_pics(self):
        # news = News.objects.get(id=1)
        url = reverse('edit_news', args=[1])
        file_source1 = 'app_news/tests/data/test_pic2.jpg'
        file_source2 = 'app_news/tests/data/test_pic3.jpg'
        with open(file_source1, 'rb') as fp1, open(file_source2, 'rb') as fp2:
            form = {'title': 'Edited name', 'description': 'Text of news.',
                    'published_at': '2022-01-05', 'file_field': [fp1, fp2]}
            response = self.client.post(url, form)
        self.assertEqual(response.status_code, 200)
        news = News.objects.get(id=1)
        self.assertEqual(news.title, 'Edited name')
        self.assertEqual(news.pictures.count(), 2)
        for pic in news.pictures.all():
            if os.path.isfile(pic.file.path):
                os.remove(pic.file.path)

    def test_edit_post_form_delete_pics(self):
        news = News.objects.get(id=1)
        file_source = 'app_news/tests/data/test_pic1.jpg'
        with open(file_source, 'rb') as fp:
            FileBlogPicture.objects.create(file=File(fp, name=os.path.basename(fp.name)), news=news)
        pic_to_del = FileBlogPicture.objects.get(id=1).file
        url = reverse('edit_news', args=[1])
        form = {'delete_pic': 1, 'pic_id': 1}
        response = self.client.post(url, form)
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        news = News.objects.get(id=1)
        self.assertEqual(news.pictures.count(), 0)
        self.assertFalse(os.path.isfile(pic_to_del.path))  # файл должен был быть удален


class TestEditPostWithoutAuth(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(username=USERNAME)
        user.set_password(USER_PASSWORD)
        user.save()
        News.objects.create(title='Title_entry', description='Text of news.',
                        published_at='2022-01-05', author=user, fl_ready_to_publish=False)

    def test_edit_url_exists(self):
        url = reverse('edit_news', args=[1])
        response = self.client.get(url)
        url_login = reverse('login')[:-1]
        url_next = f'{url_login}?next={url}'
        self.assertRedirects(response, url_next, status_code=302, target_status_code=301)

    def test_edit_post_form_without_auth(self):
        url = reverse('edit_news', args=[1])
        form = {'title': 'Edited name', 'description': 'Text of news.',
                'published_at': '2022-01-05'}
        response = self.client.post(url, form)
        url_login = reverse('login')[:-1]
        url_next = f'{url_login}?next={url}'
        self.assertRedirects(response, url_next, status_code=302, target_status_code=301)
        news = News.objects.get(id=1)
        self.assertEqual(news.title, 'Title_entry')
