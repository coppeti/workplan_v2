from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .forms import ActivityForm, EventAddForm, EventEditForm
from .models import Activities, Events
from .utils import activity_to_css

@user_passes_test(lambda u: u.is_superuser)
def activities(request):
    return render(request, 'events/activities.html')


@user_passes_test(lambda u: u.is_superuser)
def activities_list(request):
    activities = Activities.objects.all().order_by('name')
    return render(request, 'events/activities_list.html', {'activities': activities})
    

@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
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
    
  
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["POST"])
def activity_delete(request, pk):
    activity = get_object_or_404(Activities, pk=pk)
    if request.method == 'POST':
        activity.delete()
        messages.error(request, f'{activity.name} wurde gelöscht.')
        return HttpResponse(status=204, headers={'HX-Trigger': 'activitiesListChanged'})


@user_passes_test(lambda u: u.is_superuser)
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
        form = EventAddForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event {event.activity_id} erfolgreich hinzugefügt.')
            return HttpResponse(status=204, headers={'HX-Trigger': 'eventsListChanged'}) 
    else:
        form = EventAddForm()
    return render(request, 'events/event_add_form.html', {'form': form})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Events, pk=pk)
    if request.method == 'POST':
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'{event.activity_id} von {event.user_id} geändert.')
            return HttpResponse(status=204, headers={'HX-Trigger': 'eventsListChanged'})
    else:
        form = EventEditForm(instance=event)
    return render(request, 'events/event_edit_form.html', {
        'form': form,
        'event': event,
    })


@login_required
@require_http_methods(["POST"])
def event_delete(request, pk):
    event = get_object_or_404(Events, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.error(request, f'{event.activity_id} von {event.user_id} wurde gelöscht.')
        return HttpResponse(status=204, headers={'HX-Trigger': 'eventsListChanged'})
    


@login_required
def event_search(request):
    search_text = request.POST.get('search_event')
    events = Events.objects.all()
    events = Events.objects.filter(Q(user_id__last_name__icontains=search_text) |
                                    Q(user_id__first_name__icontains=search_text) |
                                    Q(activity_id__name__icontains=search_text))
    return render(request, 'events/events_list.html', {'events': events})
