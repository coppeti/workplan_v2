from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, UpdateView, DeleteView, DetailView

from .forms import RegisterForm, UserPasswordResetForm, UserForgotPasswordForm, EditUserForm
from .models import CustomUser
from .utils import account_activation_token, password_reset_token


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            message = render_to_string('email/account_activation_email.html', {
                'user': user,
                'domain': settings.DEFAULT_DOMAIN,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            # Account activation's Email
            subject = f'{user.first_name.title()}, aktiviere dein Workplan-Konto'
            subject = ''.join(subject.splitlines())
            user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
            messages.warning(request, 'User angelegt. Er muss sein Konto noch aktivieren.')
            return redirect('home')
            
        else:
            return render(request, 'accounts/register.html', {'form': form})
        
    return render(request, 'accounts/register.html', {'form': RegisterForm()})


@require_http_methods(["GET"])
def activate(request, uidb64, token):
    """Check the activation token sent via mail."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
        messages.add_message(request, messages.WARNING, str(e))
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email_confirmed = True  # changing the boolean field so that the token link becomes invalid
        user.reset_password = True
        user.save()
        new_token = password_reset_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        return HttpResponseRedirect(reverse('reset', kwargs={'uidb64': uid, 'token': new_token}))
        
    else:
        messages.add_message(request, messages.WARNING, 'Account activation link is invalid.')

    return redirect('home')


def password_reset(request, pk):
    """User forgot password form view."""
    msg = ''
    if request.method == "POST":
        form = UserForgotPasswordForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            qs = CustomUser.objects.filter(email=email)

            if len(qs) > 0:
                user = qs[0]
                user.is_active = False  # User needs to be inactive for the reset password duration
                user.reset_password = True
                user.save()

            message = render_to_string('email/password_reset_email.html', {
                'user': user,
                'domain': settings.DEFAULT_DOMAIN,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            subject = f'{user.first_name.title()}, hier ist deine Aufforderung, dein Passwort zurückzusetzen'
            subject = ''.join(subject.splitlines())
            user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
            messages.add_message(request, messages.SUCCESS, 'Email {0} eingereicht.'.format(email))
            msg = 'Wenn uns diese Adresse bekannt ist, wird eine E-Mail an dein Konto gesendet.'
        else:
            messages.add_message(request, messages.WARNING, 'Email not submitted.')
            return render(request, 'accounts/pw_reset_request.html', {'form': form})

    return render(request, 'accounts/pw_reset_request.html', {'form': UserForgotPasswordForm, 'msg': msg})


def reset(request, uidb64, token):

    if request.method == 'POST':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
            messages.add_message(request, messages.WARNING, str(e))
            user = None

        if user is not None and password_reset_token.check_token(user, token):
            form = UserPasswordResetForm(user=user, data=request.POST)
            if form.is_valid():
                user = form.save()
                user.is_active = True
                user.reset_password = False
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Passwort erfolgreich geändert.')
                login(request, user)
                return redirect('home')
            else:
                context = {
                    'form': form,
                    'uid': uidb64,
                    'token': token
                }
                messages.add_message(request, messages.WARNING, 'Passwort konnte nicht geändert werden.')
                return render(request, 'accounts/pw_reset_request.html', context)
        else:
            messages.add_message(request, messages.WARNING, 'Link zum Zurücksetzen des Passworts ist ungültig.')
            messages.add_message(request, messages.WARNING, 'Bitte fordere ein neues Passwort an.')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
        messages.add_message(request, messages.WARNING, str(e))
        user = None

    if user is not None and password_reset_token.check_token(user, token):
        context = {
            'form': UserPasswordResetForm(user),
            'uid': uidb64,
            'token': token
        }
        return render(request, 'accounts/pw_reset_request.html', context)
    else:
        messages.add_message(request, messages.WARNING, 'Link zum Zurücksetzen des Passworts ist ungültig.')
        messages.add_message(request, messages.WARNING, 'Bitte fordere ein neues Passwort an.')

    return redirect('home')


class AllUsers(ListView):
    model = CustomUser
    paginate_by = 15
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        userlist = CustomUser.objects.all().order_by('last_name')
        if q:
            userlist = CustomUser.objects.filter(
                Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(username__icontains=q) | Q(email__icontains=q)
                ).order_by('last_name')
            
        return userlist
    
    
class EditUser(UpdateView):
    model  =CustomUser
    form_class = EditUserForm
    success_url = reverse_lazy('allusers')
    

class DeleteUser(DeleteView):
    model = CustomUser
    success_url = reverse_lazy('allusers')
    
    
class MyProfile(DetailView):
    model = CustomUser