from django.db import models
from django.utils.translation import gettext_lazy as _


class ShopPromotions(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title promo'))
    text_promo = models.TextField(max_length=500, verbose_name=_('text promo'))

    class Meta:
        verbose_name_plural = _('promo-s')
        verbose_name = _('promo')

class ShopItems(models.Model):
    title_item = models.CharField(max_length=100, verbose_name=_('title item'))
    text_item = models.TextField(max_length=500, verbose_name=_('text item'))
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('price'))
    img_item = models.ImageField(upload_to='images_item/', verbose_name=_('item photo'))

    class Meta:
        verbose_name_plural = _('items')
        verbose_name = _('item')
