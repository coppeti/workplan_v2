from django.contrib import admin
from django.urls import path

from cal.views import Home, Holiday
# Views to manage everything about users
from accounts.views import (
    member,
    member_list,
    member_add,
    member_edit,
    member_delete,
    member_search,
    activate,
    password_new,
    password_reset,
    MyPasswordChange,
    MyPasswordChangeDone,
    logout_view,
    Login,
    MyProfile,
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
    path('htmx/member-search/', member_search, name="member_search"),
    path('activate/<uidb64>/<token>/', activate, name="activate"),
    path('password-new/<type>/<uidb64>/<token>/', password_new, name="password_new"),
    path('password-reset/', password_reset, name="password_reset"),
    path('password-change/', MyPasswordChange.as_view(), name="my_password_change"),
    path('password-change-done/', MyPasswordChangeDone.as_view(), name="my_password_change_done"),
    path('logout/', logout_view, name="logoutview"),
    path('login/', Login.as_view(), name="login"),
    path('my_profile/', MyProfile.as_view(), name="myprofile"),
    # Django backend
    path('mgmt/', admin.site.urls),
]
