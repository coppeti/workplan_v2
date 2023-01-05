from django import forms
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm, PasswordChangeForm
from django.core.validators import RegexValidator

from .models import CustomUser


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(required=True,
                                 max_length=50,
                                 label='Vorname',
                                 validators=[RegexValidator(r'^[a-zA-ZÀ-ÿ-\'\s]*$',
                                                            message="Verwenden Sie nur Buchstaben !")],
                                 widget=forms.TextInput(attrs={'placeholder': 'John',
                                                               'style': 'text-transform: capitalize'})
                                 )
    last_name = forms.CharField(required=True,
                                max_length=50,
                                 label='Nachname',
                                 validators=[RegexValidator(r'^[a-zA-ZÀ-ÿ-\'\s]*$',
                                                            message="Verwenden Sie nur Buchstaben !")],
                                 widget=forms.TextInput(attrs={'placeholder': 'Smith',
                                                               'style': 'text-transform: capitalize'})
                                 )
    email = forms.EmailField(required=True,
                             label='Email-Adresse',
                            #  validators=[RegexValidator(r'^([A-Za-z0-9_.+-])+\@(([A-Za-z0-9-])+\.)+([A-Za-z0-9]{2,4})+$',
                            #                             message='Gib eine gültige E-Mail-Adresse ein !')],
                             widget=forms.TextInput(attrs={'placeholder': 'hannibal@ateam.com'})
                             )
    birthday = forms.DateField(label='Geburtsdatum',
                               widget=forms.TextInput(attrs={'placeholder': '23.01.1983',
                                                             'onfocus': '(this.type="date")'})
                               )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'birthday']
        

class MySetPasswordForm(SetPasswordForm):
    def save(self, *args, commit=True, **kwargs):
        user = super().save(*args, commit=False, **kwargs)
        user.is_active = True
        if commit:
            user.save()
        return user


class UserForgotPasswordForm(PasswordResetForm):
    """User forgot password, check via email form."""
    email = forms.EmailField(label='Email-Adresse',
        max_length=254,
        required=True,
        widget=forms.TextInput(
         attrs={'placeholder': 'hannibal@ateam.com',
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
            'email': 'Email-Adresse',
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


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True,
                                 max_length=50,
                                 label = 'Vorname',
                                 validators=[RegexValidator(r'^[a-zA-ZÀ-ÿ-\'\s]*$',
                                                            message="Verwenden Sie nur Buchstaben !")],
                                 widget=forms.TextInput(attrs={'style': 'text-transform: capitalize'})
                                 )
    last_name = forms.CharField(required=True,
                                max_length=50,
                                label = 'Nachname',
                                validators=[RegexValidator(r'^[a-zA-ZÀ-ÿ-\'\s]*$',
                                                            message="Verwenden Sie nur Buchstaben !")],
                                widget=forms.TextInput(attrs={'style': 'text-transform: capitalize'})
                                 )
    username = forms.CharField(required=True,
                               max_length=30,
                               label = 'Pseudo',
                               validators=[RegexValidator(r'^[a-z0-9]{3,}$',
                                                          message='Gib mindestens 3 Kleinbuchstaben und/oder Zahlen ein')])
    
    birthday = forms.DateField(required=True,
                               label = 'Geburtsdatum',
                               widget=forms.NumberInput(attrs={'type': 'date'}))

    email = forms.EmailField(required=True,
                             label = 'Email-Adresse',
                             validators=[RegexValidator(r'^([A-Za-z0-9_.+-])+\@(([A-Za-z0-9-])+\.)+([A-Za-z0-9]{2,4})+$',
                                                        message='Gib eine gültige E-Mail-Adresse ein !')],
                             widget=forms.TextInput(attrs={'style': 'text-transform: lowercase'})
                             )
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'birthday']
        
        
# class UserPasswordChangeForm(PasswordChangeForm):
    
#     class Meta:
#         model = CustomUser