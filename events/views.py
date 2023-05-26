import copy

from datetime import date, datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_http_methods


from accounts.models import CustomUser

from .forms import ActivityForm, EventAddForm, EventEditForm
from .models import Activities, Events
from .utils import activity_to_css, admin_emails

@user_passes_test(lambda u: u.role >= CustomUser.SUPERVISOR)
def activities(request):
    return render(request, 'events/activities.html')


@user_passes_test(lambda u: u.role >= CustomUser.SUPERVISOR)
def activities_list(request):
    activities = Activities.objects.all().order_by('name')
    return render(request, 'events/activities_list.html', {'activities': activities})


@user_passes_test(lambda u: u.role >= CustomUser.SUPERVISOR)
def activity_add(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save()
            activity_to_css()
            messages.success(request, f'Aktivität {activity.name} erfolgreich hinzugefügt.')
            return HttpResponse(status=204, headers={'HX-Trigger': 'activitiesListChanged'})
    else:
        form = ActivityForm()
    return render(request, 'events/activity_add_form.html', {'form': form})


@user_passes_test(lambda u: u.role >= CustomUser.SUPERVISOR)
def activity_edit(request, pk):
    activity = get_object_or_404(Activities, pk=pk)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            activity = form.save()
            activity_to_css()
            messages.success(request, f'{activity.name} geändert.')
            return HttpResponse(status=204, headers={'HX-Trigger': 'activitiesListChanged'})
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'events/activity_add_form.html', {
        'form': form,
        'activity': activity,
    })


@user_passes_test(lambda u: u.role >= CustomUser.SUPERVISOR)
@require_http_methods(["POST"])
def activity_delete(request, pk):
    activity = get_object_or_404(Activities, pk=pk)
    if request.method == 'POST':
        activity.delete()
        activity_to_css()
        messages.error(request, f'{activity.name} wurde gelöscht.')
        return HttpResponse(status=204, headers={'HX-Trigger': 'activitiesListChanged'})


@user_passes_test(lambda u: u.role >= CustomUser.SUPERVISOR)
def activity_search(request):
    search_text = request.POST.get('search_activity')

    results = Activities.objects.filter(Q(name__icontains=search_text) |
                                        Q(short_name__icontains=search_text)).order_by('name')
    return render(request, 'events/activities_list.html', {'results': results})


@login_required
def events(request):
    return render(request, 'events/events.html')


@login_required
def events_list(request):
    events = Events.objects.filter(date_stop__gte=datetime.now().strftime('%Y-%m-%d')).order_by('date_start')
    return render(request, 'events/events_list.html', {'events': events})


@login_required
def event_add(request):
    if request.method == 'POST':
        form = EventAddForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            event = form.save(commit=False)
            activity = event.activity_id.name
            event.comment = f'{event.user_id}:\n{event.activity_id} von {event.date_start.strftime("%d.%m.%Y").strip("0")} bis {event.date_stop.strftime("%d.%m.%Y").strip("0")}'
            check_events = Events.objects.filter(date_start__lte=event.date_stop, date_stop__gte=event.date_start, confirmed=True)
            event.save()
            if user.role < CustomUser.MANAGER and (activity == 'Ferien' or activity == 'Kompensation'):
                message = render_to_string('email/event_validation_email.html', {
                    'domain': settings.DEFAULT_DOMAIN,
                    'event': event,
                    'check_events': check_events,
                })
                subject = 'Ein neuer Event bittet um Ihre Aufmerksamkeit.'
                subject = ''.join(subject.splitlines())
                send_mail(subject, message, event.user_id.email, admin_emails())
            messages.success(request, f'Event {event.activity_id} erfolgreich hinzugefügt.')
            return HttpResponse(status=204, headers={'HX-Trigger': 'eventsListChanged'})
    else:
        form = EventAddForm(user=request.user)
    return render(request, 'events/event_add_form.html', {'form': form})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Events, pk=pk)
    user = request.user
    if request.method == 'POST':
        form = EventEditForm(request.POST, instance=event, user=user)
        if form.is_valid():
            old_obj = Events.objects.get(pk=event.pk)
            form.save(commit=False)
            if (event.activity_id.name == 'Dispatcher' or event.activity_id.name == 'Pikett') and user.role < CustomUser.MANAGER:
                if Events.objects.filter(user_id=event.user_id, date_start__lte=event.date_stop, date_stop__gte=event.date_start):
                    messages.error(request, f'{event.user_id} ist zu dieser Zeit bereits beschäftigt.')
                    return HttpResponse(status=204, headers={'HX-Trigger': 'eventsListChanged'})
                else:
                    message = render_to_string('email/exchange_validation_email.html', {
                        'domain': settings.DEFAULT_DOMAIN,
                        'event': event,
                        'user': user,
                    })
                    subject = 'Antrag auf Austausch von Aktivitäten.'
                    subject = ''.join(subject.splitlines())
                    send_mail(subject, message, event.user_id.email, admin_emails())
                    event.suspended = True
                    event.save()
                    messages.warning(request, f'{event.user_id} muss den Austausch noch bestätigen.')
                    return HttpResponse(status=204, headers={'HX-Trigger': 'eventsListChanged'})
            if event.activity_id.name == 'Ferien':
                if event.confirmed == True and event.is_active == True:
                    event.comment = f'{event.user_id}:\n{event.activity_id} Change: von {event.date_start.strftime("%d.%m.%Y").strip("0")} bis {event.date_stop.strftime("%d.%m.%Y").strip("0")}'
                    if (event.date_start < old_obj.date_start or event.date_stop > old_obj.date_stop):
                        event.confirmed = False
                        check_events = Events.objects.filter(date_start__lte=event.date_stop, date_stop__gte=event.date_start, confirmed=True)
                        message = render_to_string('email/event_validation_email.html', {
                            'domain': settings.DEFAULT_DOMAIN,
                            'event': event,
                            'check_events': check_events,
                        })
                        subject = 'Ein Event wurde geändert und bittet um Ihre Aufmerksamkeit.'
                        subject = ''.join(subject.splitlines())
                        send_mail(subject, message, event.user_id.email, admin_emails())
            else:
                event.comment = f'{event.user_id}:\n{event.activity_id} Change: von {event.date_start.strftime("%d.%m.%Y").strip("0")} bis {event.date_stop.strftime("%d.%m.%Y").strip("0")}'
            event.save()
            messages.success(request, f'{event.activity_id} von {event.user_id} geändert.')
            return HttpResponse(status=204, headers={'HX-Trigger': 'eventsListChanged'})
    else:
        form = EventEditForm(instance=event, user=user)
    return render(request, 'events/event_edit_form.html', {
        'form': form,
        'event': event,
        'user': user
    })


@login_required
@require_http_methods(["POST"])
def event_delete(request, pk):
    event = get_object_or_404(Events, pk=pk)
    user = request.user
    if request.method == 'POST':
        if str(event.date_start) > datetime.now().strftime('%Y-%m-%d'):
            event.delete()
            messages.error(request, f'{event.activity_id} von {event.user_id} wurde gelöscht.')
            return HttpResponse(status=204, headers={'HX-Trigger': 'eventsListChanged'})
        messages.warning(request, 'Das Event muss in der Zukunft liegen, damit es gelöscht werden kann.')
        return HttpResponse(status=204, headers={'HX-Trigger': 'eventsListChanged'})


@login_required
@require_http_methods(["POST"])
def event_multi_delete(request):
    if request.method == 'POST':
        ids = request.POST.getlist('event_check')
        for id in ids:
            event = get_object_or_404(Events, pk=id)
            event.delete()
        messages.error(request, 'Alle ausgewählten Events wurden gelöscht.')
        return HttpResponse(status=204, headers={'HX-Trigger': 'eventsListChanged'})


@login_required
@user_passes_test(lambda u: u.role >= CustomUser.SUPERVISOR)
def event_to_confirm(request, pk):
    event = get_object_or_404(Events, pk=pk)
    event.confirmed = event.is_active = event.displayed = True
    event.save()
    message = render_to_string('email/event_confirmation_email.html', {
        'domain': settings.DEFAULT_DOMAIN,
        'event': event,
    })
    subject = 'Ihr Antrag wurde bestätigt!'
    subject = ''.join(subject.splitlines())
    send_mail(subject, message, None, [event.user_id.email])
    messages.success(request, 'Das Event wurde freigegeben und der Nutzer informiert.')
    return HttpResponseRedirect(reverse('events'))


@login_required
@user_passes_test(lambda u: u.role >= CustomUser.SUPERVISOR)
def event_refused(request, pk):
    event = get_object_or_404(Events, pk=pk)
    message = render_to_string('email/event_refused_email.html', {
        'domain': settings.DEFAULT_DOMAIN,
        'event': event,
    })
    subject = 'Ihr Antrag wurde abgelehnt.'
    subject = ''.join(subject.splitlines())
    send_mail(subject, message, None, [event.user_id.email])
    event.delete()
    messages.error(request, 'Das Event wurde abgelehnt und der Nutzer informiert.')
    return HttpResponseRedirect(reverse('events'))


@login_required
def event_exchange_ok(request, pk, user):
    event = get_object_or_404(Events, pk=pk)
    old_user = get_object_or_404(CustomUser, pk=user)
    event.suspended = False
    event.comment = f'{event.user_id}:\n{event.activity_id} Change mit {old_user}: von {event.date_start.strftime("%d.%m.%Y").strip("0")} bis {event.date_stop.strftime("%d.%m.%Y").strip("0")}.'
    event.save()
    messages.success(request, 'Der Event wurde geändert.')
    message = render_to_string('email/exchange_accepted_info_email.html', {
        'domain': settings.DEFAULT_DOMAIN,
        'event': event,
        'old_user': old_user,
    })
    subject = 'Antrag auf Austausch angenommen.'
    subject = ''.join(subject.splitlines())
    send_mail(subject, message, None, [old_user.email])
    return HttpResponseRedirect(reverse('home'))


@login_required
def event_no_exchange(request, pk, user):
    event = get_object_or_404(Events, pk=pk)
    base_user = get_object_or_404(CustomUser, pk=user)
    event.displayed = event.suspended = False
    event.user_id = base_user
    event.save()
    message = render_to_string('email/exchange_refused_info_email.html', {
        'domain': settings.DEFAULT_DOMAIN,
        'event': event,
    })
    subject = 'Antrag auf Umtausch abgelehnt.'
    subject = ''.join(subject.splitlines())
    send_mail(subject, message, None, [base_user.email])
    messages.success(request, 'Antrag auf Umtausch abgelehnt.')
    return HttpResponseRedirect(reverse('home'))
