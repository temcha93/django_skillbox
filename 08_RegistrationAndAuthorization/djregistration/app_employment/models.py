from django.db import models


class Vacancy(models.Model):

    is_active = models.BooleanField(verbose_name='Активность', default=False)
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    description = models.TextField(verbose_name='Описание')
    publisher = models.CharField(verbose_name='Кто побликовал', max_length=255)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    published_at = models.DateTimeField(verbose_name='Дата публикации', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        permissions = (
            ('can_publish', 'Может публиковать'),
        )


class Resume(models.Model):

    title = models.CharField(verbose_name='Загаловок', max_length=255)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    published_at = models.DateTimeField(verbose_name='Дата публикации', null=True, blank=True)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'