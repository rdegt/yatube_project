from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        related_name='posts',
        blank=True,
        null=True,
        help_text='Choose group'
    )
    likes = models.ManyToManyField(User, related_name='post_like')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    def __str__(self):
        return self.text
    def number_of_likes(self):
        return self.likes.count()


class Group(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField(default="Без описания")
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(verbose_name='Коммент')
    created = models.DateTimeField(auto_now_add=True)


class BanList(models.Model):
        author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ban_list'
        )
        reason = models.CharField(max_length=100, null=True, blank=True)
        data_ban = models.DateTimeField(blank=True, null=True)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followee'
    )





# Create your models here.
