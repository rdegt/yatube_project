from django.shortcuts import render

# groups/views.py
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


# Главная страница
def index(request):
    template = 'posts/index.html'
    return render(request, template)


# Страница со списком постов по группам
# view принимает параметр slug из path()
def group_posts(request, slug):
    template = 'posts/group_list.html'
    return render(request, template)
