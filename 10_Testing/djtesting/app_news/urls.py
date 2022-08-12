from django.urls import path
from .views import NewsListView, NewsDetailsView, NewsCreateFormView, NewsEditFormView, add_blog_posts

urlpatterns = [
    path('', NewsListView.as_view(), name='last_news'),
    path('blog/<username>', NewsListView.as_view(), name='user_blog'),
    path('news/<int:pk>', NewsDetailsView.as_view(), name='details_news'),
    path('news/new', NewsCreateFormView.as_view(), name='create_news'),
    path('news/<int:news_id>/edit', NewsEditFormView.as_view(), name='edit_news'),
    path('update_blog', add_blog_posts, name='update_blog'),
]
