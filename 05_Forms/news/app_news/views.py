from django.contrib.auth import authenticate, login
import datetime

from django.contrib.auth.views import LogoutView
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView, CreateView, ListView, DetailView
from .forms import NewsCommentForm, AuthForm
from .models import News


class NewsCreationFormView(CreateView):
    model = News
    template_name = 'news/news_creation_page.html'
    fields = ['title', 'description']


class NewsEditFormView(UpdateView):
    model = News
    template_name = 'news/news_edit.html'
    fields = ['title', 'description', 'date_edit']
    initial = {'date_edit': datetime.datetime.now()}


class NewsListView(ListView):
    model = News
    ordering = ['-date_create']
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'


class NewsSinglePageView(DetailView):
    model = News
    template_name = 'news/news_single_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = self.object
        context['comments'] = self.object.comments.all()
        context['comment_form'] = NewsCommentForm
        return context

    def post(self, request, **kwargs):
        news_object = self.get_object()
        comment_form = NewsCommentForm(request.POST)
        if comment_form.is_valid():
            news_object.activity += 1
            new_comment = comment_form.save(commit=False)
            new_comment.news_comment = news_object
            new_comment.save()
            news_object.save()
            return HttpResponseRedirect('/news_list')
        return render(request, 'news/news_single_page.html',
                      context={'comment_form': comment_form})


class LoginView(View):
    def get(self, request):
        auth_form = AuthForm
        return render(request, 'news/login.html', context={'form': auth_form})

    def post(self, request):
        auth_form = AuthForm(request.POST)

        if auth_form.is_valid():
            username = auth_form.cleaned_data['username']
            password = auth_form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                if not (datetime.datetime.now().hour in range(22, 25) or
                        datetime.datetime.now().hour in range(0, 9)):
                    if not user.is_superuser:
                        if user.is_active:
                            login(request, user)
                            return HttpResponseRedirect('../')
                        else:
                            auth_form.add_error('__all__', 'User is inactive!')
                    else:
                        auth_form.add_error('__all__', 'User is admin!!')
                else:
                    auth_form.add_error('__all__', 'Go sleep man!')
            else:
                auth_form.add_error('__all__', 'Incorrect user data!')
        return render(request, 'news/login.html', context={'form': auth_form})


class MyLogoutView(LogoutView):
    template_name = 'news/logout.html'
    next_page = '../'