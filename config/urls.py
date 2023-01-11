from django.contrib import admin
from django.urls import path, include

from cal.views import Home, Holiday
from accounts.views import register, activate, setpassword, deleteuser, AllUsers, EditUser, MyProfile, PasswordReset


urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('holiday/<int:year>/<str:region>/', Holiday.as_view(), name="holiday"),
    # Accounts URLs
    path('register/', register, name="register"),
    path('activate/<uidb64>/<token>/', activate, name="activate"),
    path('set_password/<type>/<uidb64>/<token>/', setpassword, name="setpassword"),
    path('password_reset', PasswordReset.as_view(), name="passwordreset"),
    path('login/', include('django.contrib.auth.urls')),
    path('all_users/', AllUsers.as_view(), name="allusers"),
    path('edit_user/<int:pk>/', EditUser.as_view(), name="edituser"),
    path('delete_user/<int:pk>/', deleteuser, name="deleteuser"),
    path('my_profile/', MyProfile.as_view(), name="myprofile"),
    # Django backend
    path('mgmt/', admin.site.urls),
]
