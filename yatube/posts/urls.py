# posts/urls.py
from django.urls import path
from . import views


app_name = 'posts'
urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    # Страница groups с конвертером slug
    path('groups/<slug:slug>/', views.group_posts, name='groups_posts'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/',views.post_edit, name='post_edit'),
    path("posts/<int:post_id>/comment", views.add_comment, name="add_comment"),
    path("follow/", views.follow_index, name="follow_index"),
    path("<str:username>/follow/", views.profile_follow, name="profile_follow"), 
    path("<str:username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
    path('post-like/<int:post_id>',views.PostLike, name="post_like"),

]