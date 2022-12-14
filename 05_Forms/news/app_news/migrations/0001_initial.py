# Generated by Django 2.2 on 2022-07-26 04:42

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, verbose_name='название статьи')),
                ('description', models.CharField(max_length=10000, verbose_name='содержание статьи')),
                ('date_create', models.DateField(auto_now_add=True, verbose_name='дата публикации')),
                ('date_edit', models.DateField(default=datetime.datetime(2022, 7, 26, 10, 42, 19, 132381), verbose_name='дата редактирования')),
                ('activity', models.IntegerField(default=0, verbose_name='количество комментариев')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Новости',
                'verbose_name_plural': 'Новости',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100, verbose_name='имя пользователя')),
                ('description', models.CharField(max_length=10000, verbose_name='текст комментария')),
                ('news_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to='app_news.News', verbose_name='Новость')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]
