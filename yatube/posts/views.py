from django.shortcuts import render
from django.core.paginator import Paginator
from .forms import PostForm
from django.shortcuts import redirect

# groups/views.py
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
#get_object_or_404 получает объект из БД или возвращает ошибкуесли не найден

from .models import Post, Group, User

from django.contrib.auth.decorators import login_required
# Декоратор для зареганных пользователей

# Главная страница

def index(request):
    # в post сохранена выборка из 10 объектов модели Post
    # отсортированных по дате новые записи вверху
    # с помощью Paginator
    posts = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(posts, 10)
    n = request.GET.get('page')

    page_object = paginator.get_page(n)

    template = 'posts/index.html'
    context = {
        #'posts': page_object,
        'page_obj': page_object,
    }
    return render(request, template, context)


# Страница со списком постов по группам
# view принимает параметр slug из path()
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    # в posts сохранена выборка из 10 объектов модели Post
    # отсортированных по дате новые записи вверху filter=group
    posts = Post.objects.all().filter(group=group).order_by('-pub_date')
    paginator = Paginator(posts, 2)
    n = request.GET.get('page')
    page_object = paginator.get_page(n)

    template = 'posts/group_list.html'
    context = {
        'group': group,
        'page_obj': page_object,
    }
    return render(request, template, context)


def profile(request, username):
    human = get_object_or_404(User, username=username)
    posts = Post.objects.all().filter(author=human).order_by('-pub_date')
    paginator = Paginator(posts, 2)
    count = paginator.count
    n = request.GET.get('page')
    page_object = paginator.get_page(n)

    context = {
        'human': human,
        'page_obj': page_object,
        'number_posts': count,
    }
    return render(request, 'posts/profile.html', context)

def post_detail(request, post_id):
    posts = get_object_or_404(Post, pk=post_id)
    context = {
        'post': posts,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    #передали в форму полученные данные
    form = PostForm(request.POST)
    context = {
        'form': form,
    }
    if form.is_valid():
        #не сохраняем (commit)
        object = form.save(commit=False)
        #назначаем пользователя объекту и сохраняем его
        object.author = request.user
        object.save()
        return redirect('posts:profile', object.author)
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    human = post.author
    if human != request.user:
        return redirect('posts:post_detail', post_id)
    
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'form': form,
        'is_edit': True,
        'post' : post,
    }
    return render(request, 'posts/create_post.html', context)
    
    
    
