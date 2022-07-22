from django.urls import path
from . import views

urlpatterns = [path('', views.About.as_view(), name='advertisement'),
               path('advertisements/', views.AdvertisementListView.as_view(), name='advertisement'),
               path('about/', views.About.as_view()),
               path('advertisements/<int:pk>', views.AdvertisementDetailView.as_view(),
                    name='advertisement-detail')

]
