from django.db import models


class Item(models.Model):
    code = models.CharField(max_length=20, verbose_name='Артикул')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')


class File(models.Model):
    file = models.FileField(upload_to='files/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
