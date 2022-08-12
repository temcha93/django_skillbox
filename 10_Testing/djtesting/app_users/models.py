import os

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from app_news.models import News


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, default=None, verbose_name=_('user'))
    name = models.CharField(max_length=42, blank=True, verbose_name=_('name'))
    last_name = models.CharField(max_length=42, blank=True, verbose_name=_('last name'))
    about = models.TextField(blank=True, verbose_name=_('about'))
    phone = models.CharField(max_length=12, blank=True, verbose_name=_('phone number'))
    city = models.CharField(max_length=42, blank=True, verbose_name=_('city'))
    is_author = models.BooleanField(default=False, verbose_name=_('is author'))
    count_published = models.IntegerField(default=0, verbose_name=_('count published'))

    def user_directory_path(instance, filename):
        path = 'avatars/'
        filename = instance.user.username + '_' + filename
        return os.path.join(path, filename)

    avatar = models.FileField(upload_to=user_directory_path, blank=True, verbose_name=_('avatar'))

    def get_absolute_url(self):
        return reverse('account', args=[str(self.user.id)])

    class Meta:
        verbose_name_plural = _('profiles')
        verbose_name = _('profile')
        permissions = [
            ('set_verified', _('Verify authors')),
        ]

    def save(self, *args, **kwargs):
        if self.pk:
            this_record = Profile.objects.get(pk=self.pk)
            if this_record.avatar != self.avatar:
                this_record.avatar.delete(save=False)
        super(Profile, self).save(*args, **kwargs)

    @receiver(post_save, sender=News)
    def update_count_published(sender, instance, **kwargs):
        if instance.pk:
            author = News.objects.get(pk=instance.pk).author
            if hasattr(author, 'profile'):
                profile = author.profile
                count_news = News.objects.filter(author__exact=author,
                                                 fl_ready_to_publish__exact=True).count()
                profile.count_published = count_news
                profile.save()
