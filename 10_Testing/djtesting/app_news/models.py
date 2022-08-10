import os

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('text'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    modified_at = models.DateTimeField(auto_now=True, verbose_name=_('modified_at'))
    published_at = models.DateField(verbose_name=_('published at'), db_index=True, default=None, null=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name=_('author'))
    fl_ready_to_publish = models.BooleanField(verbose_name=_('publish to blog'))
    fl_published = models.BooleanField(default=False, verbose_name=_('for home page'))
    tag = models.ForeignKey('Tag', null=True, on_delete=models.SET_NULL, verbose_name=_('tag'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('news')
        verbose_name_plural = _('news')
        permissions = [
            ('set_published', _('Mark news as published')),
        ]


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @classmethod
    def get_tags(cls):
        res = [tag.name for tag in cls.objects.all()]
        return res

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


class Comment(models.Model):
    name = models.CharField(max_length=20, verbose_name=_('author'))
    comment = models.TextField(verbose_name=_('text'))
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='comments', verbose_name=_('news'))

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class FileBlogPicture(models.Model):
    def user_directory_path(instance, filename):
        path = 'blogs/' + instance.news.author.username
        return os.path.join(path, filename)

    file = models.FileField(upload_to=user_directory_path, verbose_name=_('file'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='pictures', verbose_name=_('news'))

    class Meta:
        verbose_name = _('blog picture')
        verbose_name_plural = _('blog pictures')
