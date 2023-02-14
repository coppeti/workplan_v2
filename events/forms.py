from django import forms
from django.core.validators import RegexValidator

from accounts.models import CustomUser

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
                                 required=True,
                                 label='Abkürzung',
                                 validators=[RegexValidator(r'^[a-zA-Z]*$',
                                                            message="Verwenden Sie nur Buchstaben!")],
                                 widget=forms.TextInput(attrs={'placeholder': 'ADF',
                                                               'style': 'text-transform: uppercase'})
                                 )
    background_color = forms.CharField(max_length=9,
                                       required=False,
                                       )
    text_color = forms.CharField(max_length=9,
                                 required=False,
                                 )
    displayed = forms.BooleanField(required=False,
                                   label='Angezeigt',
                                   initial=True,
                                   )
    
    class Meta:
        model = Activities
        fields = ['name', 'short_name', 'background_color', 'text_color', 'displayed']
        

class EventAddForm(forms.ModelForm):
    user_id = forms.ModelChoiceField(queryset=CustomUser.objects.all().order_by('last_name'))
    activity_id = forms.ModelChoiceField(queryset=Activities.objects.all().order_by('id'))
    date_start = forms.DateField(widget=forms.TextInput(attrs={'onfocus': '(this.type="date")'}))
    date_stop = forms.DateField(widget=forms.TextInput(attrs={'onfocus': '(this.type="date")'}))
    class Meta:
        model = Events
        fields = ['user_id', 'activity_id', 'date_start', 'date_stop']


class EventEditForm(forms.ModelForm):
    pass