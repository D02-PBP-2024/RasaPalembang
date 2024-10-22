from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['nama', 'username', 'password1', 'password2', 'peran']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['nama', 'deskripsi', 'foto']
