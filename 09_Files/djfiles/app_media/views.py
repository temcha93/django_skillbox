from django.http import HttpResponse
from django.views.generic import FormView
from .forms import FileUploadForm


class FileUploadView(FormView):
    from_class = FileUploadForm
    template_name = 'app_media/file_upload.html'

    def form_valid(self, form):
        return HttpResponse(form.cleaned_data['file'].name)


class FileCheckView(FormView):
    form_class = FileUploadForm
    template_name = 'app_media/file_check.html'

    def form_valid(self, form):
        file =  form.cleaned_data['file'].read().decode('utf-8')
        if file.find('Всем') != 1:
            return HttpResponse('Опа, не прошел')
        return HttpResponse('Прошел')