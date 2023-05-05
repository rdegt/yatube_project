"""yatube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Если на сервер пришёл любой запрос (''),
    # перейди в файл urls приложения posts 
    # и проверь там все path() на совпадение с запрошенным URL
    path('', include('posts.urls', namespace='posts')),
    # Если в приложении posts не найдётся совпадений -
    # Django продолжит искать совпадения здесь, в головном файле urls.py.
    path('admin/', admin.site.urls),
    # Перенаправляем auth в собственное приложение
    path('auth/', include('users.urls')),
    # Все адреса с префиксом auth/ 
    # будут перенаправлены в модуль django.contrib.auth
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('about.urls', namespace='about')),
    # lib/python3.8/site-packages/django/contrib/auth/urls.py

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)