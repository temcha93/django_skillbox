from django.test import TestCase
from django.urls import reverse
from app_shop.models import ShopItems
from app_users.models import User


ITEM = {
    'title_item': 'Black T-shirt',
    'text_item': 'For sports and everyday life!',
    'price': '450',
    'img_item': 'media/images_item/чёрная_футболка.jpg',
}

USER = {
    'username': 'TestingUser',
    'first_name': 'Michael',
    'last_name': 'Bisping',
    'password': 'zc6-XU2-DTQ-Ae6',
}

class ShopTemplateTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        ShopItems.objects.create(**ITEM)
        User.objects.create_user(**USER)

    def setUp(self):
        self.client.login(username='TestingUser', password='zc6-XU2-DTQ-Ae6')

    def test_cabinet_template(self):
        url = reverse('cabinet')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_shop/personal_cabinet.html')

    def test_list_item_template(self):
        url = reverse('list_item')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_shop/items_list.html')

    def test_top_up_balance_template(self):
        url = reverse('top_up_balance')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_shop/top_up_balance.html')

    def test_item(self):
        url = '/shop/item/1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_shop/item_detail.html')
