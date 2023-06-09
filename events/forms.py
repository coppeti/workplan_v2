from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import Q

from accounts.models import CustomUser

from .models import Activities, Events


TODAY = datetime.now()
NL = '\n'

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

    class Meta:
        model = Activities
        fields = ['name', 'short_name', 'background_color', 'text_color', 'level']


class EventAddForm(forms.ModelForm):
    user_id = forms.ModelChoiceField(required=True,
                                     label='Benutzer',
                                     queryset=CustomUser.objects.all().order_by('last_name')
                                     )
    activity_id = forms.ModelChoiceField(required=True,
                                         label='Aktivität',
                                         queryset=Activities.objects.all().order_by('id')
                                         )
    date_start = forms.CharField(required=True,
                                 label='Von',
                                 widget=forms.TextInput(attrs={'onfocus': '(this.type="date")'})
                                 )
    date_stop = forms.CharField(required=True,
                                label='Bis',
                                widget=forms.TextInput(attrs={'onfocus': '(this.type="date")'})
                                )
    confirmed = forms.BooleanField(required=False,
                                   initial=True,
                                   label='Bestätigt',
                                   )
    is_active = forms.BooleanField(required=False,
                                   initial=True,
                                   label='Aktiv',
                                   )
    displayed = forms.BooleanField(required=False,
                                   initial=True,
                                   label='Angezeigt',
                                   )

    class Meta:
        model = Events
        fields = ['user_id', 'activity_id', 'date_start', 'date_stop', 'confirmed', 'is_active', 'displayed']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if self.user.role < CustomUser.MANAGER:
            self.fields['user_id'].initial = self.user
            self.fields['user_id'].queryset = CustomUser.objects.filter(id=self.user.id)
            self.fields['activity_id'].queryset = Activities.objects.exclude(Q(level__gt=CustomUser.TECHNICIAN))
            self.fields['confirmed'].disabled = True
            self.fields['is_active'].disabled = True
            self.fields['displayed'].disabled = True
        if self.user.role >= CustomUser.MANAGER:
            self.fields['confirmed'].initial = True

    def clean(self):
        cleaned_data = super().clean()
        date_start = cleaned_data.get('date_start')
        date_stop = cleaned_data.get('date_stop')
        activity = cleaned_data.get('activity_id')
        user = cleaned_data.get('user_id')
        if date_start and date_stop and activity and user:
            if date_stop < date_start:
                raise ValidationError('Das Enddatum liegt vor dem Startdatum!')
            if self.user.role < CustomUser.SUPERVISOR and activity.name != 'Krank':
                if str(date_start) < datetime.now().strftime('%Y-%m-%d'):
                    raise ValidationError('Der Event beginnt in der Vergangenheit!')
            if self.user.role < CustomUser.MANAGER and (activity.name == 'Ferien' or activity.name == 'Kompensation'):
                self.cleaned_data['confirmed'] = False
                self.cleaned_data['displayed'] = False
            if str(date_start) < datetime.now().strftime('%Y-%m-%d'):
                self.cleaned_data['displayed'] = False
            events = Events.objects.filter(Q(user_id=user), Q(confirmed=True),
                                                Q(date_start__lte=date_stop,  date_stop__gte=date_start) |
                                                Q(date_stop__gte=date_start, date_start__lte=date_stop))
            if events:
                for e in events:
                    if (activity.name != 'Kein Pikett' and e.activity_id != 'Kein Pikett'
                        or activity.name == 'Pikett' and e.activity_id == 'Kein Pikett'
                        or activity.name == 'Kein Pikett' and e.activity_id == 'Pikett'):
                        raise ValidationError(f'Konflikt-Events:{NL}'
                                            f'{e.user_id}, {e.activity_id} vom {e.date_start.strftime("%d.%m.%Y")} bis zum {e.date_stop.strftime("%d.%m.%Y")}')
        return cleaned_data


class EventEditForm(forms.ModelForm):
    user_id = forms.ModelChoiceField(required=True,
                                     label='Benutzer',
                                     queryset=CustomUser.objects.all().order_by('last_name'),
                                     )
    activity_id = forms.ModelChoiceField(required=True,
                                         label='Aktivität',
                                         queryset=Activities.objects.all().order_by('id'),
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

    def __init__(self, *args, **kwargs):
        logged_user = kwargs.pop('user')
        event = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if logged_user.role < CustomUser.MANAGER and event.activity_id.name == 'Dispatcher':
            self.fields['activity_id'].disabled = True
            self.fields['date_start'].disabled = True
            self.fields['date_stop'].disabled = True
            self.fields['confirmed'].disabled = True
            self.fields['is_active'].disabled = True
            self.fields['displayed'].disabled = True
            self.fields['comment'].disabled = True
        if logged_user.role < CustomUser.MANAGER and event.activity_id.name != 'Dispatcher':
            self.fields['user_id'].disabled = True
            self.fields['activity_id'].disabled = True
            self.fields['confirmed'].disabled = True
            self.fields['displayed'].disabled = True
            self.fields['comment'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user_id')
        date_start = cleaned_data.get('date_start')
        date_stop = cleaned_data.get('date_stop')
        activity = cleaned_data.get('activity_id')
        if date_start and date_stop and activity and user:
            if date_stop < date_start:
                raise ValidationError('Das Enddatum liegt vor dem Startdatum!')
            if activity != 'Krank':
                if date_start < TODAY.strftime('%Y-%m-%d'):
                    raise ValidationError('Der Event beginnt in der Vergangenheit')
                if date_stop < TODAY.strftime('%Y-%m-%d'):
                    raise ValidationError('Der Event endet in der Vergangenheit')
        return cleaned_data


class EventSwapForm(forms.Form):
    demand = forms.CharField(widget=forms.Textarea,
                             required=True,
                             label='Gewünschte Veränderung')