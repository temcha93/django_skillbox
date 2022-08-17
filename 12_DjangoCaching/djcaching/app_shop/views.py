from django.http import HttpResponse
from django.shortcuts import render
from django.views import View, generic
from app_shop.forms import BalanceForm
from app_shop.models import ShopItems, ShopPromotions
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from app_users.models import User


class PersonalCabinetView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.filter(id=request.user.id)

            items_suggest_cache_key = 'items_suggest:{}'.format(request.user.username)
            items_suggest = ShopItems.objects.filter(title_item__icontains='футболка').all()[:5]
            cache_items_suggest = cache.get_or_set(items_suggest_cache_key, items_suggest, 30 * 60)

            promotions_cache_key = 'promotions:{}'.format(request.user.username)
            promotions = ShopPromotions.objects.all()
            cache_promotions = cache.get_or_set(promotions_cache_key, promotions, 30*60)

            return render(request=request, template_name='app_shop/personal_cabinet.html', context={
                                                                                                    'items_suggest':cache_items_suggest,
                                                                                                    'promotions': cache_promotions,
                                                                                                    'user': user,
                                                                                                    })
        else:
            return HttpResponse(_("I'm sorry. But this section is not available to you"))

class ListItemsView(generic.View):
    def get(self, request):
        items_list = ShopItems.objects.all()
        return render(request=request, template_name='app_shop/items_list.html', context={'items_list': items_list})

class ItemDetailView(View):
    def get(self, request, pk):
        item = ShopItems.objects.get(id=pk)
        return render(request=request, template_name='app_shop/item_detail.html', context={'item': item})

    def post(self, request, pk):
        item = ShopItems.objects.get(id=pk)
        user = User.objects.get(id=request.user.id)
        if request.user.is_authenticated:
            if user.cash_balance - item.price >= 0:
                user.cash_balance = user.cash_balance - item.price
                user.purchases.add(item)
                user.save()
                return HttpResponse(_('Purchase completed'))
            else:
                return HttpResponse(_('The purchase cannot be made because you do not have enough funds. Please top up your account balance and try again.'))
        else:
            return HttpResponse(_('Sorry. The purchase is available only to authorized users.'))

class TopUpBalance(View):
    def get(self, request):
        form = BalanceForm()
        return render(request=request, template_name='app_shop/top_up_balance.html', context={'form': form})

    def post(self, request):
        balance_form = BalanceForm(request.POST)

        if balance_form.is_valid():
            user = User.objects.get(id=request.user.id)
            balance = balance_form.cleaned_data['balance']
            user.cash_balance = user.cash_balance + balance
            user.save()
            return HttpResponse(_('The balance has been successfully topped up'))

        return render(request=request, template_name='app_shop/top_up_balance.html', context={'form': balance_form})