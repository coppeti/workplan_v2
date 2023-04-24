from datetime import datetime

from .models import Events


def sidebar_events(request):
    today = datetime.now()
    return {'dispatcher_event': Events.objects.filter(activity_id__name='Dispatcher',
                                                      is_active=True,
                                                      confirmed=True,
                                                      date_start__lte=today.strftime('%Y-%m-%d'),
                                                      date_stop__gte=today.strftime('%Y-%m-%d')),
            'pikett_event': Events.objects.filter(activity_id__name='Pikett',
                                                  is_active=True,
                                                  confirmed=True,
                                                  date_start__lte=today.strftime('%Y-%m-%d'),
                                                  date_stop__gte=today.strftime('%Y-%m-%d')),
            'vacation_event': Events.objects.filter(activity_id__name='Ferien',
                                                    is_active=True,
                                                    confirmed=True,
                                                    date_start__lte=today.strftime('%Y-%m-%d'),
                                                    date_stop__gte=today.strftime('%Y-%m-%d')).order_by('id'),
            'compensation_event': Events.objects.filter(activity_id__name='Kompensation',
                                                        is_active=True,
                                                        confirmed=True,
                                                        date_start__lte=today.strftime('%Y-%m-%d'),
                                                        date_stop__gte=today.strftime('%Y-%m-%d')).order_by('id'),
            'other_event': Events.objects.filter(is_active=True,
                                                 confirmed=True,
                                                 date_start__lte=today.strftime('%Y-%m-%d'),
                                                 date_stop__gte=today.strftime('%Y-%m-%d'),).exclude(
                                                     activity_id__name='Dispatcher').exclude(
                                                         activity_id__name='Pikett').exclude(
                                                             activity_id__name='Ferien').exclude(
                                                                 activity_id__name='Kompensation').order_by('id')
            }