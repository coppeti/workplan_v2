from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import SignUpForm

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        birthday = request.POST.get('birthday')
        User.objects.create(first_name=first_name, last_name=last_name, email=email, birthday=birthday)
        messages.success(request, 'User saved !')
        return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form':form})
    
    
