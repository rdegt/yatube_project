from django.shortcuts import render
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import DetailView
from users.forms import UserUpdateForm, ProfileUpdateForm

# groups/views.py
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
#get_object_or_404 получает объект из БД или возвращает ошибкуесли не найден

from .models import Post, Group, User, Follow, Comment
from users.models import Profile

from django.contrib.auth.decorators import login_required
# Декоратор для зареганных пользователей

# Главная страница

def index(request):
    # в post сохранена выборка из 10 объектов модели Post
    # отсортированных по дате новые записи вверху
    # с помощью Paginator
    posts = Post.objects.all().order_by('-pub_date')
    groups = Group.objects.all()[:5]
    paginator = Paginator(posts, 10)
    n = request.GET.get('page')
    page_object = paginator.get_page(n)
    template = 'posts/index.html'
    context = {
        #'posts': page_object,
        'page_obj': page_object,
        'groups': groups,
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
    is_follower = request.user.is_authenticated and request.user.follower.filter(author=human).exists()

    context = {
        'human': human,
        'page_obj': page_object,
        'number_posts': count,
        'is_follower': is_follower,
    }
    return render(request, 'posts/profile.html', context)



# def show(request, pk):
#     users = Profile.objects.filter(id=pk)
#     context = {
#         'page_user': users,
#     }
#     return render(request, 'posts/user_profile.html', context)

def show(request, pk):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('posts:user_profile', pk)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'posts/user_profile.html', context)


def post_detail(request, post_id):
    posts = get_object_or_404(Post, pk=post_id)
    comments = posts.comments.all()
    # пустая форма для комментария
    form = CommentForm()
    liked = False
    if posts.likes.filter(id=request.user.id).exists():
        liked = True
    context = {
        'post': posts,
        'comments':comments,
        'form': form,
        'post_is_liked': liked,
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
    if human != request.user and not request.user.is_superuser:
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


@login_required
def follow_index(request):
    # информация о текущем пользователе доступна в переменной request.user
    # ...
    human = request.user
    posts = Post.objects.all().filter(author__followee__user=human).order_by('-pub_date')

    paginator = Paginator(posts, 10)
    n = request.GET.get("page") # какой номер страницы запрашивает польз
    page_object  = paginator.get_page(n)
    context = {
        'page_obj': page_object ,
    }
    return render(request, "posts/follow.html", context)

@login_required
def profile_follow(request, username):
    if request.user.username == username:
        return redirect('posts:profile', username)
    # username - строка, поэтому получаем объект
    followee = get_object_or_404(User, username=username)
    if Follow.objects.filter(user=request.user, author=followee).exists():
        messages.add_message(request, messages.SUCCESS, 'Вы уже подписаны')
    else:
        Follow.objects.create(user=request.user, author=followee)
        messages.add_message(request, messages.SUCCESS, 'Вы подписались')
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    if request.user.username == username:
        return redirect('posts:profile', username)
    followee = get_object_or_404(User, username=username)
    object = Follow.objects.filter(user=request.user, author=followee)
    if not object.exists():
        messages.add_message(request, messages.SUCCESS, 'Вы не подписывались')
    else:
        object.delete()
        messages.add_message(request, messages.SUCCESS, 'Вы отписались')
    return redirect('posts:profile', username)

  
def PostLike(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('posts:post_detail', post_id)

@login_required
def liked_index(request):
    human = request.user
    posts = Post.objects.all().filter(likes__username=human).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    n = request.GET.get("page") # какой номер страницы запрашивает польз
    page_object  = paginator.get_page(n)
    context = {
        'page_obj': page_object ,
    }
    return render(request, "posts/liked_post.html", context)


@login_required
def delete_post(request, post_id):
    human = request.user
    post = get_object_or_404(Post, pk=post_id) 
    if human == post.author or human.is_superuser or human.is_staff:
        if (human.is_staff and not human.is_superuser and post.author.is_superuser):
            messages.add_message(request, messages.SUCCESS, 'Нельзя удалить пост админа')
            return redirect('posts:index')
        post.delete()
        messages.add_message(request, messages.SUCCESS, 'Пост удален')
    else:
         messages.add_message(request, messages.SUCCESS, 'Недостаточно прав')

    return redirect('posts:index')


@login_required
def delete_comment(request, comment_id):
    human = request.user
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.pk
    if human == comment.author or human.is_superuser or human.is_staff:
        if human.is_staff and comment.author.is_superuser:
            messages.add_message(request, messages.SUCCESS, 'Нельзя удалить комм админа')
            return redirect('posts:post_detail', post_id)
        comment.delete()
    messages.add_message(request, messages.SUCCESS, 'Комментарий удален')
    return redirect('posts:post_detail', post_id)
