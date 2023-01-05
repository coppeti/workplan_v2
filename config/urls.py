from django.contrib import admin
from django.urls import path, include

from cal.views import Home, Holiday
from accounts.views import register, activate, setpassword, passwordresetdone, AllUsers, EditUser, DeleteUser, MyProfile, PasswordReset#, PasswordChange 


urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('holiday/<int:year>/<str:region>/', Holiday.as_view(), name="holiday"),
    path('register/', register, name="register"),
    path('activate/<uidb64>/<token>/', activate, name="activate"),
    path('set_password/<type>/<uidb64>/<token>/', setpassword, name="setpassword"),
    # path('password_confirm/<str:user>/', PasswordConfirm.as_view(), name="passwordconfirm"),
    path('login/', include('django.contrib.auth.urls')),
    path('password_reset/', PasswordReset.as_view(), name="password_reset"),
    path('password_reset_done/<uidb64>/', passwordresetdone, name="passwordresetdone"),
    # path('password_change/', PasswordChange.as_view(), name="passwordchange"),
    # path('password_reset', passwordreset, name="passwordreset"),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('allusers/', AllUsers.as_view(), name="allusers"),
    path('edituser/<int:pk>/', EditUser.as_view(), name="edituser"),
    path('deleteuser/<int:pk>/', DeleteUser.as_view(), name="deleteuser"),
    path('myprofile/', MyProfile.as_view(), name="myprofile"),
    path('mgmt/', admin.site.urls),
]
