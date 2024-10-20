from django.contrib.auth.forms import UserCreationForm
from .models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['nama', 'username', 'password1', 'password2', 'peran']
