from django import forms
from django.core.validators import RegexValidator
from django.db.models import Q

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
        fields = ['name', 'short_name', 'background_color', 'text_color', 'level', 'displayed']


class EventAddForm(forms.ModelForm):
    user_id = forms.ModelChoiceField(required=True,
                                     label='Benutzer',
                                     queryset=CustomUser.objects.all().order_by('last_name')
                                     )
    activity_id = forms.ModelChoiceField(required=True,
                                         label='Aktivität',
                                         queryset=Activities.objects.filter(displayed=True).order_by('id')
                                         )
    date_start = forms.CharField(required=True,
                                 label='Von',
                                 widget=forms.TextInput(attrs={'onfocus': '(this.type="date")'})
                                 )
    date_stop = forms.CharField(required=True,
                                label='Bis',
                                widget=forms.TextInput(attrs={'onfocus': '(this.type="date")'})
                                )
    class Meta:
        model = Events
        fields = ['user_id', 'activity_id', 'date_start', 'date_stop']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        user_role = self.user.role
        if user_role < CustomUser.MANAGER:
            self.fields['activity_id'].queryset = Activities.objects.exclude(Q(level__gt=CustomUser.TECHNICIAN))



class EventEditForm(forms.ModelForm):
    user_id = forms.ModelChoiceField(required=True,
                                     label='Benutzer',
                                     queryset=CustomUser.objects.all().order_by('last_name'),
                                     )
    activity_id = forms.ModelChoiceField(required=True,
                                         label='Aktivität',
                                         queryset=Activities.objects.filter(displayed=True).order_by('id'),
                                         )
    date_start = forms.CharField(required=True,
                                 label='Von',
                                 widget=forms.NumberInput(attrs={'type': 'date'}),
                                 )
    date_stop = forms.CharField(required=True,
                                label='Bis',
                                widget=forms.NumberInput(attrs={'type': 'date'}),
                                )
    confirmed = forms.BooleanField(required=False,
                                   label='Bestätigt',
                                   )
    is_active = forms.BooleanField(required=False,
                                   label='Aktiv',
                                   )
    displayed = forms.BooleanField(required=False,
                                   label='Angezeigt',
                                   )
    comment = forms.CharField(required=False,
                             label='Kommentar',
                             widget=forms.Textarea(attrs={'rows':'3'}),
                             )
    class Meta:
        model = Events
        fields = ['user_id', 'activity_id', 'date_start', 'date_stop', 'confirmed', 'is_active', 'displayed', 'comment']
