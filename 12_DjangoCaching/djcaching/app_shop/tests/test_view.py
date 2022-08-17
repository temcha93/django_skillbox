from django.test import TestCase
from django.urls import reverse
from app_shop.models import ShopItems
from app_users.models import User


USER = {
    'username': 'TestingUser',
    'first_name': 'Michael',
    'last_name': 'Bisping',
    'password': 'zc6-XU2-DTQ-Ae6',
}

ITEM = {
    'title_item': 'Black T-shirt',
    'text_item': 'For sports and everyday life!',
    'price': '450',
    'img_item': 'media/images_item/чёрная_футболка.jpg',
}


class ShopViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.item = ShopItems.objects.create(**ITEM)
        cls.user = User.objects.create_user(**USER)

    def setUp(self):
        self.client.login(username='TestingUser', password='zc6-XU2-DTQ-Ae6')

    def test_balance_and_item_detail_view(self):
        url = reverse('top_up_balance')
        data = {'balance': ['450']}
        response = self.client.post(url, data)
        user = User.objects.first()
        self.assertEqual(user.cash_balance, 450)

        url = '/shop/item/1'
        response = self.client.post(url)
        user = User.objects.first()
        self.assertEqual(user.purchases.all().count(), 1)
        self.assertContains(response, 'Purchase completed')
        self.assertEqual(float(user.cash_balance), 0)