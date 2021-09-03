from django.http import HttpResponse

from django.views import View


class ToDoView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('<ol>'
                            '<li>Установить python, выполнено</li>'
                            '<li>Установить django, сделал</li>'
                            '<li>Запустить сервер, все работает</li>'
                            '<li>Порадоваться результату, рад</li>'
                            '<li>Мне кажется у меня лишняя папка создалась в репозитории</li>'
                            '</ol>')