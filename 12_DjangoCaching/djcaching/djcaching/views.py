from django.views import View
from django.shortcuts import render


class MainPageView(View):

    def get(self, request):
        return render(request=request, template_name='main.html')