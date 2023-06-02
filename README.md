
# Социальная сеть


## Технологии

- Python 3.7
- Django 2.2.19


http://prakt.pythonanywhere.com

### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- В папке с файлом manage.py создайте миграции
```
python3 manage.py makemigrations
```
```
python3 manage.py migrate
```
- Создайте профиль админа
```
python3 manage.py createsuperuser
```
- Выполните команду:
```
python3 manage.py runserver
```
