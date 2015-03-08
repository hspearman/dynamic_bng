from django.shortcuts import render

__author__ = 'Hannah'


def home(request):
    return render(request, 'application.html', {})