from datetime import datetime

from django.shortcuts import render
from datetime import datetime, date
from django.views.generic import TemplateView

from events.models import Activities
from holidays.holidays import Holidays

from .utils import CustomCalendar


def home(request):
    this_year = datetime.now().year
    context = {
        'activities': Activities.objects.all().order_by('id'),
        'iterator': range(1,32),
        'today': datetime.now().day,
        'years': [this_year - 1, this_year, this_year + 1, this_year + 2],
        'this_year': this_year,
    }
    if request.method == 'POST':
        selected_year = int(request.POST.get('year'))
        context['selected_year'] = selected_year
        context['cal'] = CustomCalendar().formatyear(selected_year)
        return render(request, 'home.html', context)
    else:
        context['selected_year'] = this_year
        context['cal'] = CustomCalendar().formatyear(this_year)
        return render(request, 'home.html', context)


class Holiday(TemplateView):
    template_name = 'holiday.html'

    def get_context_data(self, **kwargs):
        all_regions = ['ag', 'so', 'be', 'ne', 'fr', 'vd', 'ge', 'vs', 'bs-bl']
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
