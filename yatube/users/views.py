from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Profile

# будем ссылаться на неё во view-классе
from .forms import CreationForm

class SignUp(CreateView):
    model = Profile
    form_class = CreationForm
    # перенаправляем пользователя на главную страницу
    template_name = 'users/signup.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    success_url = reverse_lazy('posts:index')

    #Данные отправленные через форму будут переданы в модель User и сохранены в БД