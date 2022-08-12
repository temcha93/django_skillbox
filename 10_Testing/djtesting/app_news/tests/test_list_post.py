import os

from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import TestCase
from django.urls import reverse

from app_news.models import News, FileBlogPicture

USERNAME = 'test'
USER_PASSWORD = 'xdrthnjil'


class TestViewBlog(TestCase):
    @classmethod
    def setUpTestData(cls):
        # три опубликованных записи (одна из них с картинкой, другая с двумя картинками), и одна неопубликованная
        user = get_user_model().objects.create(username=USERNAME)
        user.set_password(USER_PASSWORD)
        user.save()
        # self.client.force_login(user)
        News.objects.create(title='Title_entry', description='Text of news.',
                            published_at='2022-01-05', author=user, fl_ready_to_publish=True)
        news = News.objects.get(id=1)
        file_source = 'app_news/tests/data/test_pic1.jpg'
        with open(file_source, 'rb') as fp:
            FileBlogPicture.objects.create(file=File(fp, name=os.path.basename(fp.name)), news=news)
        News.objects.create(title='Entry 2', description='Something very important.',
                            published_at='2022-01-11', author=user, fl_ready_to_publish=True)
        news = News.objects.get(id=2)
        file_source = 'app_news/tests/data/test_pic2.jpg'
        with open(file_source, 'rb') as fp:
            FileBlogPicture.objects.create(file=File(fp, name=os.path.basename(fp.name)), news=news)
        file_source = 'app_news/tests/data/test_pic3.jpg'
        with open(file_source, 'rb') as fp:
            FileBlogPicture.objects.create(file=File(fp, name=os.path.basename(fp.name)), news=news)
        News.objects.create(title='Happy New Year', description='Walk, drink, sleep.',
                            published_at='2022-01-01', author=user, fl_ready_to_publish=False)
        News.objects.create(title='Happy New Year', description='Доброго утра всем, кто проснулся. '
                                                                'Волшебных снов всем, кто спит. '
                                                                'Драйва и отличного настроения тем, кто жив. '
                                                                'И воскрешения - тем, кто не.',
                            published_at='2022-01-01', author=user, fl_ready_to_publish=True)

    @classmethod
    def tearDownClass(cls):
        pics_to_del = FileBlogPicture.objects.all()
        for pic in pics_to_del:
            if os.path.isfile(pic.file.path):
                os.remove(pic.file.path)
        super(TestViewBlog, cls).tearDownClass()  # Call parent last

    def test_url_blog_exists(self):
        url = reverse('user_blog', args=[USERNAME])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_news/news_list.html')
        author = get_user_model().objects.get(username=USERNAME)
        news = News.objects.filter(fl_ready_to_publish__exact=True, author=author).all().order_by('-published_at')
        self.assertListEqual(list(response.context['news']), list(news))

    def test_list_has_right_links(self):
        url = reverse('user_blog', args=[USERNAME])
        response = self.client.get(url)
        for i in [1, 2, 4]:
            url_detail = reverse('details_news', args=[i])
            news = News.objects.get(id=i)
            self.assertContains(response, url_detail)
            self.assertContains(response, news.title)
            self.assertContains(response, news.author.username)
            self.assertContains(response, news.description[:99])
        url_detail = reverse('details_news', args=[3])
        self.assertNotContains(response, url_detail)

    def test_post_detail_has_full_text(self):
        url = reverse('details_news', args=[4])
        response = self.client.get(url)
        news = News.objects.get(id=4)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, news.title)
        self.assertContains(response, news.author.username)
        self.assertContains(response, news.description)

    def test_post_not_published_not_allowed(self):
        url = reverse('details_news', args=[3])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The news has not yet been published')

    def test_post_detail_has_pictures(self):
        for i in [1, 2]:
            url = reverse('details_news', args=[i])
            response = self.client.get(url)
            news = News.objects.get(id=i)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, news.title)
            self.assertContains(response, news.author.username)
            self.assertContains(response, news.description)
            for pic in news.pictures.all():
                self.assertContains(response, pic.file.url)
