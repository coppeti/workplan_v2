from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.views.decorators.http import require_http_methods

from .forms import ActivityForm
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
