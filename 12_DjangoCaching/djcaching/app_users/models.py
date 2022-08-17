from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from app_shop.models import ShopItems


class User(AbstractUser):
    first_name = models.CharField(max_length=30, default='', verbose_name=_('first name'))
    last_name = models.CharField(max_length=30, default='', verbose_name=_('last name'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('birthday'))
    city = models.CharField(max_length=30, default='', verbose_name=_('city'))
    cash_balance = models.DecimalField(max_digits=100, decimal_places=2, default=0, verbose_name=_('cash balance'))
    purchases = models.ManyToManyField(ShopItems, related_name='purchases')

    class Meta:
        verbose_name_plural = _('users')
        verbose_name = _('user')
