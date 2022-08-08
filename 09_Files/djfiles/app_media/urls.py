from django.urls import path

from app_media import views

urlpatterns = [
    path('', views.FileUploadView.as_view(), name='file_upload'),
    path('check/', views.FileCheckView.as_view(), name='file_check'),
]