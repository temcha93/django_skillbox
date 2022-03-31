from django.shortcuts import render
from django.http import HttpResponse


def advertisement_list(request, *args, **kwargs):
    return render(request, 'advertisement/advertisement_list.html', {})


def course1(request, *args, **kwargs):
    return render(request, 'advertisement/course1.html', {})


def course2(request, *args, **kwargs):
    return render(request, 'advertisement/course2.html', {})


def course3(request, *args, **kwargs):
    return render(request, 'advertisement/course3.html', {})


def course4(request, *args, **kwargs):
    return render(request, 'advertisement/course4.html', {})


def course5(request, *args, **kwargs):
    return render(request, 'advertisement/course5.html', {})