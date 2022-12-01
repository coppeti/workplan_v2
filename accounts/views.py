from django.shortcuts import render

from .forms import SignupForm


def signup(request):
    form = SignupForm()
    
    return render(request, 'signup.html', {'form':form})
