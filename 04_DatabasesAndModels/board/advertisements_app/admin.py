from django.contrib import admin
from .models import Advertisement, AdvertisementUser


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    pass


@admin.register(AdvertisementUser)
class AdvertisementAdmin(admin.ModelAdmin):
    pass
