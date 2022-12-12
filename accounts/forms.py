from django import forms
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.core.validators import RegexValidator

from .models import CustomUser


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(required=True,
                                 max_length=50,
                                 label='Vorname',
                                 validators=[RegexValidator(r'^[a-zA-ZÀ-ÿ-\'\s]*$',
                                                            message="Verwenden Sie nur Buchstaben !")],
                                 widget=forms.TextInput(attrs={'placeholder': 'Vorname',
                                                               'style': 'text-transform: capitalize'})
                                 )
    last_name = forms.CharField(required=True,
                                max_length=50,
                                 label='Nachname',
                                 validators=[RegexValidator(r'^[a-zA-ZÀ-ÿ-\'\s]*$',
                                                            message="Verwenden Sie nur Buchstaben !")],
                                 widget=forms.TextInput(attrs={'placeholder': 'Nachname',
                                                               'style': 'text-transform: capitalize'})
                                 )
    email = forms.EmailField(required=True,
                             label='Email',
                             validators=[RegexValidator(r'^([A-Za-z0-9_.+-])+\@(([A-Za-z0-9-])+\.)+([A-Za-z0-9]{2,4})+$',
                                                        message='Gib eine gültige E-Mail-Adresse ein !')],
                             widget=forms.TextInput(attrs={'placeholder': 'Email'})
                             )
    birthday = forms.DateField(label='Geburtsdatum',
                               widget=forms.NumberInput(attrs={'type': 'date'})
                               )
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'birthday']


class UserPasswordResetForm(SetPasswordForm):
    """Change password form."""
    new_password1 = forms.CharField(label='Passwort',
        help_text="<ul class='errorlist text-muted'>\
            <li>Dein Passwort darf deinen anderen persönlichen Daten nicht zu ähnlich sein.</li>\
                <li>Dein Passwort muss mindestens 8 Zeichen enthalten.</li>\
                    <li>Dein Passwort darf kein häufig verwendetes Passwort sein.</li>\
                        <li>Dein Passwort darf nicht ausschließlich aus Zahlen bestehen.<li></ul>",
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Passwort',
            'type': 'password',
            'id': 'user_password',
        }))

    new_password2 = forms.CharField(label='Kontrollpasswort',
        help_text=False,
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Kontrollpasswort',
            'type': 'password',
            'id': 'user_password',
        }))
    

class UserForgotPasswordForm(PasswordResetForm):
    """User forgot password, check via email form."""
    email = forms.EmailField(label='Email',
        max_length=254,
        required=True,
        widget=forms.TextInput(
         attrs={'placeholder': 'email address',
                'type': 'text',
                'id': 'email_address'
                }
        ))
    
    
class EditUserForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'birthday', 'is_active', 'is_staff', 'is_superuser']
        labels= {
            'first_name': 'Vorname',
            'last_name': 'Nachname',
            'username': 'Pseudo',
            'email': 'Email',
            'birthday': 'Geburtsdatum',
            'is_active': 'Ist aktiv',
            'is_staff': 'Ist Administrator',
            'is_superuser': 'Ist Superuser',
        }
        
        widgets = {
            'birthday': forms.NumberInput(
                attrs={'type': 'date'}
            )
        }
