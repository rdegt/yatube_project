from django.contrib import admin

from .models import Post
from .models import Group

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group')  #отображение в админке
    list_editable = ('group',) #позволит менять поле group в любом посте
    search_fields = ('text',)  #поиск по тексту
    list_filter = ('pub_date',) #фильтр по дате
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'slug',
        'description',
    )
    empty_value_display = '-пусто-'
    list_filter = ('title',)
    search_fields = ('title',)
    empty_value_display = '-пусто-'

admin.site.register(Post, PostAdmin)

admin.site.register(Group, GroupAdmin)




# Register your models here.
