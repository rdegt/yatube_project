from django.shortcuts import render

# groups/views.py
from django.http import HttpResponse


# Главная страница
def index(request):    
    return HttpResponse('Главная страница')


# Страница со списком постов по группам
# view принимает параметр slug из path()
def group_posts(request, slug):
    return HttpResponse(f'Список постов по группе {slug}')
