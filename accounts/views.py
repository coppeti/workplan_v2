from django.shortcuts import render, redirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.template.loader import render_to_string
from django.views.generic import TemplateView
# from django.http import HttpResponseRedirect
from django.contrib import messages
# from django.contrib.auth import get_user_model

from .forms import RegisterForm

# User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = settings.DEFAULT_DOMAIN
            context = {
                'user': user,
                'domain': current_site,
                'uid': uid,
                'token': token,
                'timout_days': settings.PASSWORD_RESET_TIMEOUT_DAYS,
            }
            # Account activation's Email
            subject = f'{user.first_name.title()}, aktiviere dein Workplan-Konto'
            subject = ''.join(subject.splitlines())
            message = render_to_string('email/account_activation_email.html', context)
            user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
            messages.warning(request, 'User angelegt. Er muss sein Konto noch aktivieren.')
            return redirect('home')
            
        else:
            context = {'form': form}
            return render(request, 'register.html', context)
        
        messages.success(request, 'User saved !')
        return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form':form})


class Activate(TemplateView):
    pass
