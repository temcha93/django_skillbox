from django.contrib import admin
from .models import Comment, News, FileBlogPicture


class FileBlogPictureInLine(admin.TabularInline):
    model = FileBlogPicture


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at', 'author', 'fl_ready_to_publish', 'fl_published', 'tag']
    inlines = [FileBlogPictureInLine]


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'comment', 'news']


@admin.register(FileBlogPicture)
class FileBlogPictureAdmin(admin.ModelAdmin):
    list_display = ['news', 'created_at']
