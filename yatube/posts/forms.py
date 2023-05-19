from django import forms
from .models import Post, Comment
from django.forms import  Textarea


class PostForm(forms.ModelForm):
    class Meta:
        #класс, на основе которого создается форма
        model = Post
        fields = ('text', 'group', 'image')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, help_text='Ваше имя')
    email = forms.EmailField(help_text='email')
    topic = forms.CharField(max_length=50)
    text = forms.CharField(widget=forms.Textarea, max_length=1000)


class SearchForm(forms.Form):
    text = forms.CharField(max_length=100)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'rows': 3})
        }

