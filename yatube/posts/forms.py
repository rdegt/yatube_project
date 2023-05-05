from django import forms
from .models import Post 


class PostForm(forms.ModelForm):
    class Meta:
        #класс, на основе которого создается форма
        model = Post
        fields = ('text', 'group')