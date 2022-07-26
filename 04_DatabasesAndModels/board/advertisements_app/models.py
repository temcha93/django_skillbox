from unicodedata import category

from django.db import models
from datetime import datetime
from pycbrf.toolbox import ExchangeRates

date_now = datetime.now().strftime('%Y-%m-%d')
rate = ExchangeRates(date_now)['USD'].rate


class Advertisement(models.Model):
    title = models.CharField(max_length=1000, verbose_name='Заголовок объявления')
    description = models.CharField(max_length=1000, default='', verbose_name='Описание')
    price = models.IntegerField(default=0, verbose_name='Цена')
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    publication_end_date = models.DateField(verbose_name='Дата окончания публикации')
    views_count = models.IntegerField(default=0, verbose_name='')
    user_adv = models.ForeignKey('AdvertisementUser', on_delete=models.CASCADE,
                                 related_name='advertisements',
                                 verbose_name='Автор объявления')
    category_adv = models.ForeignKey('AdvertisementCategory', on_delete=models.CASCADE,
                                     related_name='advertisements',
                                     verbose_name='Рубрика')
    type_adv = models.ForeignKey('AdvertisementType', on_delete=models.CASCADE,
                                     related_name='advertisements',
                                     verbose_name='Тип Объявления')

    def get_price_usd(self):
        return round(self.price / rate, 2)

    price_usd = property(get_price_usd)

    def __str__(self):
        return self.title


class AdvertisementUser(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='E-mail')
    phone = models.IntegerField(verbose_name='Телефон')

    def __str__(self):
        return self.name


class AdvertisementCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AdvertisementType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
