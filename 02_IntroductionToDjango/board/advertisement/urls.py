from django.urls import path
from .import views

urlpatterns = [
    path('', views.advertisement_list, name='advertisement_list'),
    path('advertisement1/', views.advertisement1, name='advertisement1')

]