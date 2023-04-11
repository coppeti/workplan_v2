from datetime import datetime

from django.shortcuts import render
from datetime import datetime, date
from django.views.generic import TemplateView

from events.models import Activities
from holidays.holidays import Holidays

from .utils import CustomCalendar


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = datetime.now().year
        context['activities'] = Activities.objects.all().order_by('id')
        context['cal'] = CustomCalendar().formatyear(year)
        context['iterator'] = range(1,32)
        context['today'] = datetime.now().day
        return context


class Holiday(TemplateView):
    template_name = 'holiday.html'

    def get_context_data(self, **kwargs):
        all_regions = ['ag', 'so', 'be', 'ne', 'fr', 'vd', 'ge']
        context = super().get_context_data(**kwargs)
        context['year'] = kwargs['year']
        context['prev_year'] = context['year'] - 1
        context['next_year'] = context['year'] + 1
        context['year_after'] = date.today().year + 1
        context['region'] = kwargs['region']
        context['regions'] = all_regions.copy()
        context['regions'].remove(context['region'])
        context['holidays'] = Holidays(context['year'], context['region']).hdays()
        return context
