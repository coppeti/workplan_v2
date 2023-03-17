from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from accounts.models import CustomUser

from .forms import ActivityForm, EventAddForm, EventEditForm
from .models import Activities, Events
from .utils import activity_to_css

@user_passes_test(lambda u: u.role >= CustomUser.ADMIN)
def activities(request):
    return render(request, 'events/activities.html')


@user_passes_test(lambda u: u.role >= CustomUser.ADMIN)
def activities_list(request):
    activities = Activities.objects.all().order_by('name')
    return render(request, 'events/activities_list.html', {'activities': activities})


@user_passes_test(lambda u: u.role >= CustomUser.ADMIN)
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


@user_passes_test(lambda u: u.role >= CustomUser.ADMIN)
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


@user_passes_test(lambda u: u.role >= CustomUser.ADMIN)
@require_http_methods(["POST"])
def activity_delete(request, pk):
    activity = get_object_or_404(Activities, pk=pk)
    if request.method == 'POST':
        activity.delete()
        messages.error(request, f'{activity.name} wurde gelöscht.')
        return HttpResponse(status=204, headers={'HX-Trigger': 'activitiesListChanged'})


@user_passes_test(lambda u: u.role >= CustomUser.ADMIN)
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
    events = Events.objects.all().order_by('date_start')
    return render(request, 'events/events_list.html', {'events': events})


@login_required
def event_add(request):
    if request.method == 'POST':
        form = EventAddForm(request.POST, user=request.user)
        if form.is_valid():
            event = form.save(commit=False)
            if event.activity_id.level >= 4:
                event.confirmed = event.is_active = event.displayed = True
            event.comment = f'{event.user_id}:\n{event.activity_id} von {event.date_start.strftime("%d.%m.%Y").strip("0")} bis {event.date_stop.strftime("%d.%m.%Y").strip("0")}'
            event.save()
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
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
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
    if request.method == 'POST':
        event.is_active = False
        event.save()
        messages.error(request, f'{event.activity_id} von {event.user_id} wurde gelöscht.')
        return HttpResponse(status=204, headers={'HX-Trigger': 'eventsListChanged'})


@login_required
@require_http_methods(["POST"])
def event_multi_delete(request):
    if request.method == 'POST':
        ids = request.POST.getlist('event_check')
        for id in ids:
            event = get_object_or_404(Events, pk=id)
            event.is_active = False
            event.save()
        messages.error(request, 'Alle ausgewählten Events wurden gelöscht.')
        return HttpResponse(status=204, headers={'HX-Trigger': 'eventsListChanged'})


@login_required
@user_passes_test(lambda u: u.role >= CustomUser.ADMIN)
def event_permanent_removal(request):
    lastYear = date.today().year - 1
    oldEvents = Events.objects.filter(date_stop__year__lte=lastYear, is_active=False, confirmed=False)
    if request.method == 'POST':
        oldEvents.delete()
        messages.error(request, 'Alle alten Events wurden aus der Datenbank gelöscht.')
        return HttpResponseRedirect(reverse('events'))
    else:
        return render(request, 'events/event_permanent_removal.html', {'oldEvents': oldEvents})