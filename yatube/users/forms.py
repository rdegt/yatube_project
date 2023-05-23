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


class BanForm(forms.Form):
    CHOICE = [
        ("0 min", "0 min - разблокировка"),
        ("2 min", "2 min"), 
        ('60 min', '60 min'), 
        ('1140 min', '1440 min')
    ]
    reason = forms.CharField(max_length=100, help_text='Причина блокировки')
    time_ban = forms.ChoiceField(choices=CHOICE)