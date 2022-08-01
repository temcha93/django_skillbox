from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsListView.as_view()),
    path('news_creation_page/', views.NewsCreationFormView.as_view(success_url="/news_list/")),
    path('news/<int:pk>/news_edit/', views.NewsEditFormView.as_view(success_url="/news_list/")),
    path('news/<int:pk>/news_single_page/', views.NewsSinglePageView.as_view(), name='news_pk'),
    path('news_list/', views.NewsListView.as_view(), name='news_list'),
    path('login/', views.LoginView.as_view(), name='login_news'),
    path('logout/', views.MyLogoutView.as_view(), name='logout_news'),

]