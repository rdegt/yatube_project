from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.contrib.messages import get_messages
from ..models import Group, Post

User = get_user_model()

class PostViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='user_auth')
        cls.group = Group.objects.create(title='Тест группа', 
                                         slug='testslug', 
                                         description='Тестовое описание',)
        cls.post = Post.objects.create(text='Текст',author=cls.user,)

        cls.guest_client = Client()
        cls.AUTHOR = Client()
        cls.AUTHOR.force_login(cls.user)
        cls.testuser = User.objects.create(username='account')
        cls.TEST_USER = Client()
        cls.TEST_USER.force_login(cls.testuser)

    # Проверяем используемые шаблоны
    def test_uses_correct_template(self):
        "Используются правильные шаблоны."
        templates = {
            reverse('posts:groups_posts', kwargs={'slug':PostViewTests.group.slug}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': PostViewTests.user}): 'posts/profile.html',
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_detail', kwargs={'post_id': PostViewTests.post.id}): 
                    'posts/post_detail.html',
            reverse('posts:add_comment', kwargs={'post_id': PostViewTests.post.id}): 
                    'posts/post_detail.html',
            reverse('posts:follow_index'): 'posts/follow.html',
            reverse('posts:liked_post'): 'posts/liked_post.html',

            #reverse('posts:post_edit', kwargs={'post_id':PostViewTests.post.id}): 'posts/create_post.html'
        }
        for name, template in templates.items():
            with self.subTest(name=name):
                response = self.TEST_USER.get(name)
                self.assertTemplateUsed(response, template)
    

    def test_uses_corret_template_for_edit(self):
        "Используется верный шаблон если автор редактирует свой пост"
        tmp = reverse('posts:post_edit', kwargs={'post_id':PostViewTests.post.id})
        response = self.AUTHOR.get(tmp)
        self.assertTemplateUsed(response, 'posts/create_post.html')
    
    




        