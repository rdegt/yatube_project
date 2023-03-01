# posts/urls.py
from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    # Страница groups с конвертером slug
    path('groups/<slug:slug>/', views.group_posts, name='groups_posts'),

]