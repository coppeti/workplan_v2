from django.contrib import admin
from django.urls import path, include

from cal.views import Home, Holiday
# Views to manage everything about users
from accounts.views import (
    member,
    member_list,
    member_add,
    member_edit,
    member_delete,
    # register,
    activate,
    setpassword,
    deleteuser,
    logout_view,
    Login,
    AllUsers,
    # EditUser,
    MyProfile,
    PasswordReset,
    logout_view)


urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('holiday/<int:year>/<str:region>/', Holiday.as_view(), name="holiday"),
    # Accounts URLs
    path('member/', member, name="member"),
    path('htmx/member-list/', member_list, name="member_list"),
    path('htmx/member-add/', member_add, name="member_add"),
    path('htmx/member/<pk>/edit/', member_edit, name="member_edit"),
    path('htmy/member/<pk>/delete/', member_delete, name="member_delete"),
    # path('register/', register, name="register"),
    path('activate/<uidb64>/<token>/', activate, name="activate"),
    path('set_password/<type>/<uidb64>/<token>/', setpassword, name="setpassword"),
    path('password_reset/', PasswordReset.as_view(), name="passwordreset"),
    path('password_change/', include('django.contrib.auth.urls')),
    path('logout/', logout_view, name="logoutview"),
    path('login/', Login.as_view(), name="login"),
    path('all_users/', AllUsers.as_view(), name="allusers"),
    # path('edit_user/<int:pk>/', EditUser.as_view(), name="edituser"),
    path('delete_user/<int:pk>/', deleteuser, name="deleteuser"),
    path('my_profile/', MyProfile.as_view(), name="myprofile"),
    # Django backend
    path('mgmt/', admin.site.urls),
]
