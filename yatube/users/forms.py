from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


# класс для формы регистрации унаследуя от встроенного класса регистрации
class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # поля при регистрации 
        fields = ('first_name', 'last_name', 'username', 'email')