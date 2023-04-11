from django.shortcuts import render

# groups/views.py
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
#get_object_or_404 получает объект из БД или возвращает ошибкуесли не найден

from .models import Post, Group


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
    group = get_object_or_404(Group, slug=slug)
    # в posts сохранена выборка из 10 объектов модели Post
    # отсортированных по дате новые записи вверху filter=group
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'posts': posts
    }
    return render(request, template, context)