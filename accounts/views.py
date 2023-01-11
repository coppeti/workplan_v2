from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView
from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, UpdateView

from .forms import RegisterForm, UserForgotPasswordForm, EditUserForm, EditProfileForm, MySetPasswordForm
from .models import CustomUser


@user_passes_test(lambda u: u.is_superuser)
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.username = f'{user.first_name[:2]}{user.last_name[:2]}'
            user.save()
            message = render_to_string('email/account_activation_email.html', {
                'user': user,
                'domain': settings.DEFAULT_DOMAIN,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
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

    if user is not None and default_token_generator.check_token(user, token):
        user.email_confirmed = True  # changing the boolean field so that the token link becomes invalid
        user.save()
        new_token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        type = 'new'
        return HttpResponseRedirect(reverse('setpassword', kwargs={'type': type, 'uidb64': uid, 'token': new_token}))
    else:
        messages.add_message(request, messages.WARNING, 'Account activation link is invalid.')

    return redirect('home')


def setpassword(request, type, uidb64, token):
    if request.method == 'POST':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
            
        if user is not None and default_token_generator.check_token(user, token):
            form = MySetPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                password = request.POST['new_password1']
                user.set_password(password)
                user.save()
                login(request, user)
                return redirect('home')
        else:
            context = {
                'form': form,
                'uid': uidb64,
                'token': token,
                'type': type
            }
            return render(request, 'accounts/set_new_password.html', context)
    else:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
            
        if user is not None and default_token_generator.check_token(user, token):
            context = {
                'form': MySetPasswordForm(user),
                'uid': uidb64,
                'token': token,
                'user': user,
                'type': type
            }
            return render(request, 'accounts/set_new_password.html', context)
        
    return redirect('home')


class PasswordReset(PasswordResetView):
    form_class = UserForgotPasswordForm
    email_template_name = 'email/password_reset_email.html'
    
    
class AllUsers(UserPassesTestMixin, ListView):
    model = CustomUser
    paginate_by = 15
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        userlist = CustomUser.objects.all().order_by('last_name')
        if q:
            userlist = CustomUser.objects.filter(
                Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(username__icontains=q) | Q(email__icontains=q)
                ).order_by('last_name')
            
        return userlist
    
    
class EditUser(UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = EditUserForm
    success_url = reverse_lazy('allusers')

    def test_func(self):
        return self.request.user.is_superuser
    

@user_passes_test(lambda u: u.is_superuser)
def deleteuser(request, pk):
    user = CustomUser.objects.get(id=pk)
    user.delete()
    messages.success(request, "Der Benutzer wurde gelöscht.")
    return HttpResponseRedirect(reverse_lazy('allusers'))


class MyProfile(UpdateView):
    model = CustomUser
    template_name = 'accounts/myprofile_form.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('home')
    
    def get_object(self):
        return self.request.user
