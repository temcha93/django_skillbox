from django.contrib.auth.forms import UserCreationForm
from django.forms import HiddenInput
from app_users.models import User


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'date_of_birth', 'city')
        widgets = {
            'cash_balance': HiddenInput(),
            'purchases': HiddenInput(),
        }
