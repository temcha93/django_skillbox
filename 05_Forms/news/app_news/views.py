import datetime
from pyexpat import model

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView, CreateView, ListView, DetailView
from .forms import NewsCommentForm
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
            return HttpResponseRedirect(reverse('news_list'))
        return render(request, 'news/news_single_page.html',
                      context={'comment_form': comment_form})
