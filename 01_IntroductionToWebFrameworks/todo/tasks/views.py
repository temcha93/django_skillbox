from django.http import HttpResponse
from random import shuffle
from django.views import View


class ToDoView(View):

    def get(self, request, *args, **kwargs):


        list = ['Установить python, выполнено',
                'Установить django, сделал',
                'Запустить сервер, все работает',
                'Порадоваться результату, рад'
                ]
        shuffle(list)
        items = ''
        for s in list:
            items += f'<li>{s}</li>'
        result = '<html><body><ol>%s</ol></body></html>' % items
        return HttpResponse(result)