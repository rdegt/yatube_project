from django.shortcuts import render

# groups/views.py
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Post


# Главная страница
def index(request):
    # в post сохранена выборка из 10 объектов модели Post
    # отсортированных по дате новые записи вверху
    posts = Post.objects.order_by('-pub_date')[:10]
    template = 'posts/index.html'
    context = {
        'posts': posts,
    }
    return render(request, template, context)


# Страница со списком постов по группам
# view принимает параметр slug из path()
def group_posts(request, slug):
    template = 'posts/group_list.html'
    context = {
        'text': "Здесь будет информация о группах проекта Yatube",
    }
    return render(request, template, context)