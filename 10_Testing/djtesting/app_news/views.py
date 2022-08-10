import os
from _csv import reader

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import News, Tag, Comment, FileBlogPicture
from .forms import NewsForm, CommentForm, UploadCSVFileForm


@method_decorator([login_required, permission_required('app_news.set_published')], name='post')
class NewsListView(generic.ListView):
    model = News
    context_object_name = 'news'

    def get_queryset(self):
        mode = self.request.GET.get('mode')
        if mode == 'author' and self.request.user.is_authenticated:  # and self.request.user.profile.is_author:
            return News.objects.filter(fl_ready_to_publish__exact=False,
                                       author__exact=self.request.user). \
                order_by('published_at')

        if mode == 'moder' and self.request.user.has_perm('app_news.set_published'):
            return News.objects.filter(fl_published__exact=False, fl_ready_to_publish__exact=True). \
                order_by('published_at')

        fl_base_str = True
        filters = {}  # {'fl_published__exact': True}
        tag_name = self.request.GET.get('tag')
        if tag_name:
            tag = Tag.objects.filter(name=tag_name).first()
            if tag:
                filters['tag'] = tag
                fl_base_str = False
        username = self.kwargs.get('username')
        if username:
            author = User.objects.get(username=username)
            if author:
                filters['author'] = author
                fl_base_str = False
        date = self.request.GET.get('date')
        if date:
            filters['published_at__exact'] = date
            fl_base_str = False
        else:  # можно было бы для личных блогов показывать записи из будущих дат, как "прикрепленные сверху"
            now = timezone.now()
            filters['published_at__lte'] = now
        if fl_base_str:  # без дополнительных фильтров показываем только записи для главной
            filters['fl_published__exact'] = True
        else:  # с фильтрами - записи, опубликованные в блогах
            filters['fl_ready_to_publish__exact'] = True
        return News.objects.filter(**filters).order_by('-published_at')

    def post(self, request):
        news = get_object_or_404(News, pk=request.POST['news_id'])
        if news.fl_ready_to_publish and not news.fl_published:
            author = news.author
            news.fl_published = True
            news.save()
            if author:
                profile = author.profile
                profile.count_published = profile.count_published + 1
                profile.save()
        return HttpResponseRedirect(reverse('last_news') + '?mode=moder')


class NewsDetailsView(generic.DetailView):
    model = News

    def dispatch(self, request, pk, *args, **kwargs):
        news = get_object_or_404(News, pk=pk)
        if not news.fl_ready_to_publish:
            return render(request, 'app_news/error_news.html',
                          {'error_message': _('The news has not yet been published')})
        return super().dispatch(request, pk, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_comment'] = CommentForm(
            initial={'name': self.request.user.username if self.request.user.is_authenticated else ''})
        return context

    def post(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comment(news=news, **comment_form.cleaned_data)
            comment.save()
            return HttpResponseRedirect(reverse('details_news', args=[news.pk]))
        return render(request, 'app_news/news_detail.html',
                      {'news': news, 'form_comment': CommentForm()})


def author_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.profile.is_author:
            raise PermissionDenied
        return func(request, *args, **kwargs)

    return wrapper


@method_decorator([login_required], name='dispatch')
class NewsEditFormView(View):

    def dispatch(self, request, news_id, *args, **kwargs):
        news = get_object_or_404(News, pk=news_id)
        if not (news.author == request.user):
            return render(request, 'app_news/error_news.html', {'error_message': _('Not your news, not you and edit')})
        elif news.fl_published:
            return render(request, 'app_news/error_news.html',
                          {'error_message': _('The news has already been published')})
        else:
            return super().dispatch(request, news_id, *args, **kwargs)

    def get(self, request, news_id):
        news = get_object_or_404(News, pk=news_id)
        news_form = NewsForm(instance=news, data_list=Tag.get_tags(),
                             initial={'tag': news.tag.name if news.tag else ''})
        return render(request, 'app_news/new_news.html', {'news_form': news_form, 'news': news})

    def post(self, request, news_id):
        news = get_object_or_404(News, pk=news_id)
        if 'delete_pic' in request.POST:
            file = FileBlogPicture.objects.get(id=request.POST['pic_id'])
            if file.news == news:
                if os.path.isfile(file.file.path):
                    os.remove(file.file.path)
                file.delete()
            return HttpResponseRedirect(reverse('edit_news', args=[news_id]))
        news_form = NewsForm(request.POST, request.FILES, instance=news, data_list=Tag.get_tags())
        if news_form.is_valid():
            tag_name = news_form.cleaned_data['tag']
            news_form.cleaned_data['tag'] = None
            if len(tag_name) > 0:
                tag, fl = Tag.objects.get_or_create(name=tag_name)
                news.tag = tag
            else:
                news.tag = None
            news.save()
            files = request.FILES.getlist('file_field')
            for f in files:
                picture = FileBlogPicture(file=f, news=news)
                picture.save()
        return render(request, 'app_news/new_news.html', {'news_form': news_form, 'news': news})


@method_decorator([login_required], name='dispatch')
class NewsCreateFormView(View):

    def get(self, request):
        news_form = NewsForm(data_list=Tag.get_tags())
        return render(request, 'app_news/new_news.html', {'news_form': news_form})

    def post(self, request):
        news_form = NewsForm(request.POST, request.FILES, data_list=Tag.get_tags())
        if news_form.is_valid():
            tag = None
            tag_name = news_form.cleaned_data['tag']
            if len(tag_name) > 0:
                tag, fl = Tag.objects.get_or_create(name=tag_name)
            new_post = News(title=news_form.cleaned_data['title'],
                            description=news_form.cleaned_data['description'],
                            published_at=news_form.cleaned_data['published_at'],
                            fl_ready_to_publish=news_form.cleaned_data['fl_ready_to_publish'],
                            author=request.user,
                            tag=tag)  # **news_form.cleaned_data)
            new_post.save()
            files = request.FILES.getlist('file_field')
            for f in files:
                picture = FileBlogPicture(file=f, news=new_post)
                picture.save()
            return HttpResponseRedirect(reverse('edit_news', args=[new_post.pk]))
        return render(request, 'app_news/new_news.html', {'news_form': news_form})


@login_required
def add_blog_posts(request):
    if request.method == 'POST':
        upload_file_form = UploadCSVFileForm(request.POST, request.FILES)
        if upload_file_form.is_valid():
            file = upload_file_form.cleaned_data['file']
            data = file.read().decode('utf-8').split('\n')
            csv_reader = reader(data, delimiter=';', quotechar='"')
            counter = 0
            for row in csv_reader:
                try:
                    description = row[0]
                    published_at = datetime.strptime(row[1], "%Y-%m-%d")
                except:  # ошибка парсинга даты публикации, либо колонок меньше двух
                    description = None
                    published_at = None
                if description and published_at:
                    new_post = News(title=_("Draft"),
                                    description=description,
                                    published_at=published_at,
                                    fl_ready_to_publish=False,
                                    author=request.user)
                    new_post.save()
                    counter += 1
            if counter > 0:
                return HttpResponseRedirect(reverse('last_news') + '?mode=author')
            else:
                upload_file_form.add_error('file',
                                           _('Check the file format. There seems to be something wrong with it.'))
    else:
        upload_file_form = UploadCSVFileForm()

    context = {
        'form': upload_file_form
    }
    return render(request, 'app_news/uppend_blog.html', context=context)
