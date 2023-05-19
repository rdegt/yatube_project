# Импортируем из приложения django.contrib.auth нужный view-класс
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView 
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from . import views
from django.urls import reverse_lazy

app_name = 'users'

urlpatterns = [
    path(
      'logout/',
        # шаблон должен применяться для отображения возвращаемой страницы.
      LogoutView.as_view(template_name='users/logged_out.html'),
      name='logout'
    ),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
     path(
        'password_reset/',
        PasswordResetView.as_view(template_name='users/password_reset_form.html', 
                                  success_url = reverse_lazy('users:password_reset_done')),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html', 
                                         success_url = reverse_lazy('users:reset_complete')),
        name='reset_letter'
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='reset_complete'
    ),
    path(
        'password_change/',
        PasswordChangeView.as_view(template_name='users/password_change_form.html',success_url = reverse_lazy('users:password_change_done')),
        name='password_change'
    ),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
        name='password_change_done'
    ),

]