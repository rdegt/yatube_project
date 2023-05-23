from django.contrib import admin
from .models import BanInAuth
# Register your models here.

class BanInAuthAdmin(admin.ModelAdmin):
    list_display = (
        'count',
        'ip',
        'is_ban',
        'time',
        )  #отображение в админке

admin.site.register(BanInAuth) 
