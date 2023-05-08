from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile
from django import forms


User = get_user_model()


# класс для формы регистрации унаследуя от встроенного класса регистрации
class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # поля при регистрации 
        fields = ('first_name', 'last_name', 'username', 'email')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'tg']