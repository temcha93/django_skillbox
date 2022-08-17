from django.urls import path
from app_shop.views import PersonalCabinetView, ListItemsView, ItemDetailView, TopUpBalance

urlpatterns = [
    path('cabinet/', PersonalCabinetView.as_view(), name='cabinet'),
    path('list_item/', ListItemsView.as_view(), name='list_item'),
    path('item/<int:pk>', ItemDetailView.as_view()),
    path('top_up_balance/', TopUpBalance.as_view(), name='top_up_balance'),
]
