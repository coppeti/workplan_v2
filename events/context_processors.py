from datetime import datetime

from .models import Events


def sidebar_events(request):
    today = datetime.now()
    return {'s_events': Events.objects.filter(confirmed='True',
                                              date_start__lte=today.strftime('%Y-%m-%d'),
                                              date_stop__gte=today.strftime('%Y-%m-%d')).order_by('id')}