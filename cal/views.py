from django.shortcuts import render
from datetime import datetime
from django.views.generic import TemplateView

# def home(request):
#     context = {}
#     context['day_iterator'] = range(1,32)
#     context['this_date'] = datetime.now().day
#     return render(request, 'home.html', context)


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['iterator'] = range(1,32)
        context['today'] = datetime.now().day
        return context

    
