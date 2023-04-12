from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

# будем ссылаться на неё во view-классе
from .forms import CreationForm

class SignUp(CreateView):
    form_class = CreationForm
    # перенаправляем пользователя на главную страницу
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'
    #Данные отправленные через форму будут переданы в модель User и сохранены в БД