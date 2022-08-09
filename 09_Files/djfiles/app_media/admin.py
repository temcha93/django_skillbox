from django.contrib import admin
from .models import *


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'price')


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
