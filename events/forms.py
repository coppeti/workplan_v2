from django import forms
from django.core.validators import RegexValidator

from .models import Activities, Events


class ActivityForm(forms.ModelForm):
    name = forms.CharField(max_length=50,
                           required=True,
                           label='Name',
                           validators=[RegexValidator(r'^[a-zA-ZÀ-ÿ\-\/\s]*$',
                                                      message="Verwenden Sie nur Buchstaben, \"-\" und \"/\"!")],
                           widget=forms.TextInput(attrs={'placeholder': 'Auf der Flucht',
                                                         'style': 'text-transform: capitalize'})
                           )
    short_name = forms.CharField(max_length=3,
                                 required=3,
                                 label='Abkürzung',
                                 validators=[RegexValidator(r'^[a-zA-Z]*$',
                                                            message="Verwenden Sie nur Buchstaben!")],
                                 widget=forms.TextInput(attrs={'placeholder': 'MRT',
                                                               'style': 'text-transform: uppercase'})
                                 )
    background_color = forms.CharField(max_length=9,
                                       required=False,
                                       )
    text_color = forms.CharField(max_length=9,
                                 required=False,
                                 )
    
    class Meta:
        model = Activities
        fields = ['name', 'short_name', 'background_color', 'text_color']
        
