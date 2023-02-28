# posts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.index),
    # Страница groups с конвертером slug
    path('groups/<slug:slug>/', views.group_posts),

]