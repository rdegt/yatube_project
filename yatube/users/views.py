from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, View
from django.urls import reverse_lazy
from .models import Profile, BanInAuth
from django.shortcuts import redirect
from django.contrib import auth
from django.utils import timezone
from django.contrib import messages

# будем ссылаться на неё во view-классе
from .forms import CreationForm
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm


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



def my_login(request):
    if request.method == 'GET':
        context = {
            'form' : AuthenticationForm,
        }
        return render(request, 'users/login.html', context)
    if request.method == 'POST':
        ip = request.META.get('HTTP_X_REAL_IP')
        if not ip:
            ip = request.META.get('REMOTE_ADDR')
        object = BanInAuth.objects.all().filter(ip=ip)
        if not object.exists():
            object = BanInAuth.objects.create(ip=ip, time=timezone.now())
        else:
            object = object[0]
        form = AuthenticationForm(request, data=request.POST)
        if object.is_ban and object.time > timezone.now():
                messages.success(request, f'Вы заблокированы до {object.time}. Попробуйте войти позже')
                context = { 'form' : form, }
                return redirect('posts:index')
        elif object.is_ban and object.time <= timezone.now():
             # разблокировать его
             object.is_ban = False
             object.save()
             
        if form.is_valid():
            auth.login(request, form.get_user())
            object.delete()
            return redirect('posts:index')
        else:
             # пытается подобрать пароль
            object.count += 1
            object.save()
            if (object.count > 3):
                 object.is_ban = True
                 object.time = timezone.now() + timezone.timedelta(minutes=2)
                 messages.success(request, f'Вы заблокированы до {object.time}. Попробуйте войти позже')
                 object.save()
                 return redirect('posts:index')
        context = {
            'form' : form,
        } 
    
        return render(request, 'users/login.html', context)



