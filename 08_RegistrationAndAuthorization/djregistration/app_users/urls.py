from django.urls import path
from . import views



urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('account/', views.AccountView.as_view(), name='account'),
]