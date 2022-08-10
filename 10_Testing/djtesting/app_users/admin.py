from django.contrib import admin

# Register your models here.
from app_users.models import Profile


@admin.register(Profile)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_author', 'count_published']
