from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import CustomUser


class SignUpForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'birthday']
        required_fields = ['first_name', 'last_name', 'email', 'birthday']
        
