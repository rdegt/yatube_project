from django.shortcuts import render
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib import messages

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
    comments = posts.comments.all()
    # пустая форма для комментария
    form = CommentForm()
    context = {
        'post': posts,
        'comments':comments,
        'form': form,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    #передали в форму полученные данные
    form = PostForm(request.POST, files=request.FILES or None)
    context = {
        'form': form,
    }
    if form.is_valid():
        #не сохраняем (commit)
        object = form.save(commit=False)
        #назначаем пользователя объекту и сохраняем его
        object.author = request.user
        object.save()
        messages.add_message(request, messages.SUCCESS, 'Ваш пост размещен', extra_tags='create_post')
        return redirect('posts:profile', object.author)
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    human = post.author
    if human != request.user:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if form.is_valid():
        if (form.has_changed()):
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Успешно отредактировано')
        return redirect('posts:post_detail', post_id)
    context = {
        'form': form,
        'is_edit': True,
        'post' : post,
    }
    return render(request, 'posts/create_post.html', context)
    

@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, pk=post_id)
    human = request.user
    context = {
        'post': post,
        'form' : form,
        'comments': post.comments.all()
    }
    if form.is_valid():
        object = form.save(commit=False)
        #назначаем пользователя объекту и сохраняем его
        object.author = human
        object.post = post
        object.save()
        messages.add_message(request, messages.SUCCESS, 'Комментарий добавлен')
        return redirect('posts:post_detail', post_id)
    return render(request, 'posts/post_detail.html', context)


    
