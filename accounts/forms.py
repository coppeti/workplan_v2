import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import CustomUser


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(required=True,
                                 label='Vorname',
                                 validators=[RegexValidator(r'^[a-zA-ZÀ-ÿ-\'\s]*$',
                                                            message="Verwenden Sie nur Buchstaben !")],
                                 widget=forms.TextInput(attrs={'placeholder': 'Vorname',
                                                               'style': 'text-transform: capitalize'})
                                 )
    last_name = forms.CharField(required=True,
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


# class TestForm(forms.Form):
#     first_name = forms.CharField(required=True,
#                                  label='Prenom:',
#                                  validators=[RegexValidator(r'^[A-Za-z][A-Za-z\'\-]+([\ A-Za-z][A-Za-z\'\-]+)*',
#                                                             message="Seulement des lettres !")],
#                                  widget=forms.TextInput(attrs={'placeholder': 'Votre prénom',
#                                                                'style': 'text-transform: capitalize'})
#                                  )
#     last_name = forms.CharField(required=True,
#                                  label='Nom:',
#                                  validators=[RegexValidator(r'^[A-Za-z][A-Za-z\'\-]+([\ A-Za-z][A-Za-z\'\-]+)*',
#                                                             message="Seulement des lettres !")],
#                                  widget=forms.TextInput(attrs={'placeholder': 'Votre nom',
#                                                                'style': 'text-transform: capitalize'})
#                                  )