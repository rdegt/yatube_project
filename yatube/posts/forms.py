from django import forms
from .models import Post, Comment
from django.forms import  Textarea


class PostForm(forms.ModelForm):
    class Meta:
        #класс, на основе которого создается форма
        model = Post
        fields = ('text', 'group', 'image')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'rows': 3})
        }