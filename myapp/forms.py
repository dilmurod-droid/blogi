from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from myapp.models import CustomUser
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'gender', 'password1', 'password2','photo']
class Editpr(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'gender', 'photo']