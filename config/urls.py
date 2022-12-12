from django.contrib import admin
from django.urls import path, include

from cal.views import Home, Holiday
from accounts.views import register, activate, password_reset, reset, AllUsers, EditUser, DeleteUser, MyProfile

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('holiday/<int:year>/<str:region>/', Holiday.as_view(), name="holiday"),
    path('register/', register, name="register"),
    path('activate/<uidb64>/<token>/', activate, name="activate"),
    path('login/', include('django.contrib.auth.urls')),
    path('password_reset/', password_reset, name="password_reset"),
    path('reset/<uidb64>/<token>/', reset, name="reset"),
    path('allusers/', AllUsers.as_view(), name="allusers"),
    path('edituser/<int:pk>/', EditUser.as_view(), name="edituser"),
    path('deleteuser/<int:pk>/', DeleteUser.as_view(), name="deleteuser"),
    path('myprofile/<pk>/', MyProfile.as_view(), name="myprofile"),
    path('mgmt/', admin.site.urls),
]
