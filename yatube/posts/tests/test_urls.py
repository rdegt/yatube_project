from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from django.contrib.messages import get_messages

from ..models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')  
        self.assertEqual(response.status_code, 200)

class PostUrlTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # создаем запись в виртуальной БД для тестов
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


    def test_urls_uses_correct_template(self):
         """URL-адрес использует соответствующий шаблон для автора поста."""
         templates = {
             '/': 'posts/index.html',
             '/groups/testslug/' : 'posts/group_list.html',
             '/profile/user_auth/': 'posts/profile.html',
             f"/posts/{self.post.id}/": 'posts/post_detail.html',
             f"/posts/{self.post.id}/edit/": 'posts/create_post.html',
             '/create/': 'posts/create_post.html',
         }
         # тестируем для авторизированного пользователя, автора поста
         for address, template in templates.items():
             with self.subTest(address=address):
                response = self.AUTHOR.get(address)
                self.assertTemplateUsed(response, template) 


    def test_urls_redirect_from_edit(self):
        "Перенаправить пользователя, если пытается редактировать чужой пост."
        response = self.TEST_USER.get("/posts/1/edit/", follow=True)
        self.assertRedirects(response, '/posts/1/')
    
    def test_urls_success_crear(self):
        "Пользователь успешно создает новую запись."
        response = self.AUTHOR.get('/create/')
        self.assertEqual(response.status_code, 200)
    
    def test_urls_success_delete(self):
        "Пользователь успешно удаляет свою запись, получает сообщение."
        response = self.AUTHOR.get(f'/delete_post/{PostUrlTests.post.id}')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пост удален')

    def test_urls_not_success_delete(self):
        "Пользователь не может удалить чужую запись, получает сообщение."
        other_post = Post.objects.create(text='Тестовый',author=self.user,)
        response = self.TEST_USER.get(f'/delete_post/{other_post.id}')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Недостаточно прав')


 





