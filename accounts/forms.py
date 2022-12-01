from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'birthday',]
        required_fields = ['first_name', 'last_name', 'email', 'birthday',]
