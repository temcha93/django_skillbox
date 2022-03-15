from django.shortcuts import render
from django.http import HttpResponse


def advertisement_list(request, *args, **kwargs):
    return render(request, 'advertisement/advertisement_list.html', {})


def advertisement1(request, *args, **kwargs):
    return render(request, 'advertisement/advertisement1.html', {})