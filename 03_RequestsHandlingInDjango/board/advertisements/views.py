from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

title = 'Бесплатные объявления'
advertisements = [
    'Мастер на час',
    'Выведение из запоя',
    'Услуги экскаватора-погрузчика, гидромолота, ямобура',
    'Бурение скважин'
]
categories = [
    'Мастер на час',
    'Выведение из запоя',
    'Услуги экскаватора-погрузчика, гидромолота'
]
regions = [
    'Нижегородская область',
    'Московская область',
    'Владимирская область',
    'Республика Чувашия',
    'Республика Марий-Эл'
]


class Home(View):
    def get(self, request):
        return render(request, 'advertisements/home.html',
                      {'regions': regions, 'categories': categories,
                       'title': title})


class Advertisements(View):
    def get(self, request):
        return render(request, 'advertisements/advertisement_list.html',
                      {'advertisements': advertisements, 'title': title})

    def post(self, request):
        num_post_requests = request.session.get('num_post_requests', 0)
        request.session['num_post_requests'] = num_post_requests + 1
        msg = f'Запрос по созданию новой записи успешно выполнен<br> Всего ' \
              f'обработано {num_post_requests + 1} POST-запросов'
        return HttpResponse(msg)


class About(TemplateView):
    template_name = 'advertisements/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = title
        context['name'] = 'ООО "Пайтон адвертисментс"'
        context['description'] = """
        Расскажите о себе. Найдите поставщиков. Расширьте связи. 
        Сосредоточьтесь на бизнесе. Все необходимые инструменты доступны 
        сразу после регистрации.
        """
        return context


class Contacts(TemplateView):
    template_name = 'advertisements/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Бесплатные объявления'
        context['name'] = 'ООО "Пайтон адвертисментс"'
        context['address'] = 'г. Москва, ул. Покровка, д. 20 Б'
        context['phone'] = '+7 495 906-00-00'
        context['mail'] = 'info@adv.ru'

        return context