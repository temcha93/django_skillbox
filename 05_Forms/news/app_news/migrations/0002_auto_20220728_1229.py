# Generated by Django 2.2 on 2022-07-28 06:29

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='news_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app_news.News', verbose_name='Новость'),
        ),
        migrations.AlterField(
            model_name='news',
            name='date_edit',
            field=models.DateField(default=datetime.datetime(2022, 7, 28, 12, 29, 19, 298013), verbose_name='дата редактирования'),
        ),
    ]