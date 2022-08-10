from _csv import reader
from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from django.views import *
from .models import *


class UploadFileView(View):
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            return HttpResponse(content=file.name + ' size: ' + str(file.size), status=200)

    def get(self, request):
        form = UploadFileForm()
        return render(request, 'media/upload_file.html', context={'form': form})


def item_list(request):
    items = Item.objects.all()
    return render(request, 'media/items_list.html', {'item_list': items})


class UpdatePricesView(View):
    def post(self, request):
        form = UpdatePriceForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file = request.FILES['file'].read()
                price_str = file.decode('utf-8').split('\n')
                csv_reader = reader(price_str, delimiter=',', quotechar='"')
                for row in csv_reader:
                    Item.objects.filter(code=row[0]).update(price=Decimal(row[1]))
                return HttpResponse(content='Updated', status=200)
            except Exception as ex:
                return HttpResponse(content='Error', status=200)


    def get(self, request):
        form = UpdatePriceForm()
        return render(request, 'media/upload_price_file.html', context={'form': form})


class ModelFormUploadView(View):
    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')

    def get(self, request):
        form = DocumentForm()
        return render(request, 'media/file_form_upload.html', {'form': form})


class MultipleFilesUploadView(View):
    def post(self, request):
        form = MultiFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            for f in files:
                instance = File(file=f)
                instance.save()
            return redirect('/')

    def get(self, request):
        form = MultiFileForm()
        return render(request, 'media/upload_files.html', {'form': form})

