from django.urls import path

from .views import register_view, LoginView, account_view, LogoutView, ProfileUpdateView

urlpatterns = [
    path('registration/', register_view, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:pk>/', account_view, name='account'),
    path('<int:pk>/edit', ProfileUpdateView.as_view(), name='edit_profile'),
]
