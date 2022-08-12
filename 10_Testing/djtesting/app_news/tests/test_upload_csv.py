from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app_news.models import News

USERNAME = 'test'
USER_PASSWORD = 'xdrthnjil'


class TestUploadCSV(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(username=USERNAME)
        user.set_password(USER_PASSWORD)
        user.save()

    def setUp(self):
        user = get_user_model().objects.get(username=USERNAME)
        self.client.force_login(user)

    def test_url_upload_exists(self):
        url = reverse('update_blog')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/uppend_blog.html')

    def test_upload_works_with_correct_data(self):
        url = reverse('update_blog')
        file_source = 'app_news/tests/data/upload_test_correct_data.csv'
        with open(file_source, 'rb') as fp:
            form = {'file': [fp]}
            response = self.client.post(url, form)
            url_next = reverse('last_news')+'?mode=author'
            self.assertRedirects(response, url_next, status_code=302, target_status_code=200)
        author = get_user_model().objects.get(username=USERNAME)
        news = News.objects.filter(fl_ready_to_publish__exact=False, author=author).all()
        self.assertEqual(news.count(), 3)

    def test_upload_works_with_not_fully_correct_data(self):
        url = reverse('update_blog')
        file_source = 'app_news/tests/data/upload_test_data.csv'
        with open(file_source, 'rb') as fp:
            form = {'file': [fp]}
            response = self.client.post(url, form)
        url_next = reverse('last_news')+'?mode=author'
        self.assertRedirects(response, url_next, status_code=302, target_status_code=200)
        author = get_user_model().objects.get(username=USERNAME)
        news = News.objects.filter(fl_ready_to_publish__exact=False, author=author).all()
        self.assertEqual(news.count(), 2)
