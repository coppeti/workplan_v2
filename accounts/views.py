from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, UpdateView

from .forms import MemberAddForm, MemberEditForm, MyPasswordResetForm, EditProfileForm, PasswordNewForm
from .models import CustomUser



@user_passes_test(lambda u: u.is_superuser)
def member(request):
    return render(request, 'accounts/member.html')


def member_list(request):
    return render(request, 'accounts/member_list.html', {
        'members': CustomUser.objects.all().order_by('last_name')
        })


def member_add(request):
    if request.method == 'POST':
        form = MemberAddForm(request.POST)
        if form.is_valid():
            member = form.save()
            member.username = f'{member.first_name[:2]}{member.last_name[:2]}'
            member.save()
            message = render_to_string('email/account_activation_email.html', {
                'member': member,
                'domain': settings.DEFAULT_DOMAIN,
                'uid': urlsafe_base64_encode(force_bytes(member.pk)),
                'token': default_token_generator.make_token(member)
            })
            # Account activation's Email
            subject = f'{member.first_name.title()}, aktiviere dein Workplan-Konto'
            subject = ''.join(subject.splitlines())
            member.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
            messages.warning(request, 'User angelegt. Er muss sein Konto noch aktivieren.')
            return HttpResponse(status=204, headers={'HX-Trigger': 'memberListChanged'}) 
    else:
        form = MemberAddForm()
    return render(request, 'accounts/member_add_form.html', {'form': form})


def member_edit(request, pk):
    member = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = MemberEditForm(request.POST, instance=member)
        if form.is_valid():
            member = form.save()
            messages.success(request, f'{member.first_name.title()} {member.last_name.upper()} geändert.')
            return HttpResponse(status=204, headers={'HX-Trigger': 'memberListChanged'})
    else:
        form = MemberEditForm(instance=member)
    return render(request, 'accounts/member_edit_form.html', {
        'form': form,
        'member': member,
    })
    

@require_http_methods(["POST"])
def member_delete(request, pk):
    member = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.error(request, f'{member.first_name.title()} {member.last_name.upper()} wurde gelöscht.')
        return HttpResponse(status=204, headers={'HX-Trigger': 'memberListChanged'})
    
    
# @user_passes_test(lambda u: u.is_superuser)
# def register(request):
#     """Create a new user.
#     An email containing an activation link will be sent to the address provided during registration
#     """
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.username = f'{user.first_name[:2]}{user.last_name[:2]}'
#             user.save()
#             message = render_to_string('email/account_activation_email.html', {
#                 'user': user,
#                 'domain': settings.DEFAULT_DOMAIN,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': default_token_generator.make_token(user)
#             })
#             # Account activation's Email
#             subject = f'{user.first_name.title()}, aktiviere dein Workplan-Konto'
#             subject = ''.join(subject.splitlines())
#             user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
#             messages.warning(request, 'User angelegt. Er muss sein Konto noch aktivieren.')
#             return redirect('allusers')
#         else:
#             return render(request, 'accounts/register.html', {'form': form})
        
#     return render(request, 'accounts/register.html', {'form': RegisterForm()})


@require_http_methods(["GET"])
def activate(request, uidb64, token):
    """Check the activation token sent via mail.
    In case of validation of the token, the user is redirected to the registration form of his new password.
    """
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
        return HttpResponseRedirect(reverse('password_new', kwargs={'type': type, 'uidb64': uid, 'token': new_token}))
    else:
        messages.add_message(request, messages.WARNING, 'Account activation link is invalid.')

    return redirect('home')


def password_new(request, type, uidb64, token):
    """Propose à l'utilisateur un formulaire pour renseigner son mot de passe.
    The function is called in the process of creating a user (type = 'new') or
     in the process of requesting a password reset (type = 'reset').
    """
    if request.method == 'POST':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
            
        if user is not None and default_token_generator.check_token(user, token):
            form = PasswordNewForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                password = request.POST['new_password1']
                user.set_password(password)
                user.save()
                login(request, user)
                if type == 'new':
                    messages.success(request, f'{user.first_name.capitalize()}, dein Konto ist nun aktiv und du bist angemeldet.')
                elif type == 'reset':
                    messages.success(request, f'{user.first_name.capitalize()}, dein Passwort wurde erfolgreich zurückgesetzt und du bist angemeldet.')
                return redirect('home')
            else:
                context = {
                    'form': form,
                    'uid': uidb64,
                    'token': token,
                    'type': type
                }
                return render(request, 'accounts/password_new.html', context)
        else:
            context = {
                'form': form,
                'uid': uidb64,
                'token': token,
                'type': type
            }
            return render(request, 'accounts/password_new.html', context)
    else:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
            
        if user is not None and default_token_generator.check_token(user, token):
            context = {
                'form': PasswordNewForm(user),
                'uid': uidb64,
                'token': token,
                'user': user,
                'type': type
            }
            return render(request, 'accounts/password_new.html', context)
        
    return redirect('home')


class Login(SuccessMessageMixin, LoginView):
    """To inform the user that he is connected after the login."""
    success_message = 'Du bist jetzt angemeldet.'
    

def password_reset(request):
    form = MyPasswordResetForm()
    if request.method == 'POST':
        form = MyPasswordResetForm(request.POST)
        if form.is_valid():
            try:
                email = request.POST.get('email')
                member = CustomUser.objects.get(email=email)
            except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
                member = None
        
            if member is not None:
                member.is_active = False
                member.save()
                message = render_to_string('email/password_reset_email.html', {
                    'member': member,
                    'domain': settings.DEFAULT_DOMAIN,
                    'uid': urlsafe_base64_encode(force_bytes(member.pk)),
                    'token': default_token_generator.make_token(member)
                })
                subject = f'{member.first_name.title()}, setzt dein Passwort zurück.'
                subject = ''.join(subject.splitlines())
                member.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
                return render(request, 'registration/password_reset_done.html', {'member': member})
            else:
                return redirect('home')
        else:
            form = MyPasswordResetForm()
    
    return render(request, 'registration/password_reset_form.html', {'form': form})
                
    
# class AllUsers(UserPassesTestMixin, ListView):
#     """Displays a list of all registered users.
#     For backend user management."""
#     model = CustomUser
#     paginate_by = 15
    
#     # Access only for Superuser 
#     def test_func(self):
#         return self.request.user.is_superuser
    
#     # Displays the result of the search field
#     def get_queryset(self):
#         q = self.request.GET.get('q')
#         userlist = CustomUser.objects.all().order_by('last_name')
#         if q:
#             userlist = CustomUser.objects.filter(
#                 Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(username__icontains=q) | Q(email__icontains=q)
#                 ).order_by('last_name')
            
#         return userlist
    
    
# class EditUser(UserPassesTestMixin, UpdateView):
#     """Editing a registered user.
#     Access to complete information, backend, only for Superuser."""
#     model = CustomUser
#     form_class = EditUserForm
#     success_url = reverse_lazy('allusers')

#     def test_func(self):
#         return self.request.user.is_superuser
    

# @user_passes_test(lambda u: u.is_superuser)
# def deleteuser(request, pk):
#     """Deleting a user.
#     Backend, only for Superuser."""
#     user = CustomUser.objects.get(id=pk)
#     user.delete()
#     messages.success(request, "Der Benutzer wurde gelöscht.")
#     return HttpResponseRedirect(reverse_lazy('allusers'))


class MyProfile(SuccessMessageMixin, UpdateView):
    """Displays the profile of the logged user.
    Only the basic information can be changed:
        First name, last name, username, date of birth.
    The password can be changed from this view."""
    model = CustomUser
    template_name = 'accounts/myprofile_form.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('home')
    success_message = 'Dein Profil wurde erfolgreich aktualisiert.'
    
    def get_object(self):
        return self.request.user


def logout_view(request):
    """To inform the user of his disconnection."""
    logout(request)
    messages.success(request, 'Du bist jetzt abgemeldet.')
    return redirect('home')