from django.urls import path
from .import views
import os

urlpatterns = [
    path('upload_file/', views.UploadFileView.as_view(), name='upload_file'),
    path('goods/', views.item_list, name='item_list'),
    path('prices/', views.UpdatePricesView.as_view(), name='prices'),
    path('model_upload/', views.ModelFormUploadView.as_view(), name='model_upload'),
    path('upload_files/', views.MultipleFilesUploadView.as_view(), name='upload_files'),

]