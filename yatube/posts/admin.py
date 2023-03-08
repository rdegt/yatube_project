from django.contrib import admin

from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author')  #отображение в админке
    search_fields = ('text',)  #поиск по тексту
    list_filter = ('pub_date',) #фильтр по дате
    empty_value_display = '-пусто-'



admin.site.register(Post, PostAdmin)



# Register your models here.
