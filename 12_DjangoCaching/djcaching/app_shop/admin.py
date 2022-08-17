from django.contrib import admin
from app_shop.models import ShopPromotions, ShopItems


class PromotionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'text_promo')
admin.site.register(ShopPromotions, PromotionsAdmin)


class ItemsAdmin(admin.ModelAdmin):
    list_display = ('title_item', 'text_item', 'price', 'img_item')
admin.site.register(ShopItems, ItemsAdmin)
