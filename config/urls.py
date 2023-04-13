from django.contrib import admin
from django.urls import path

# Landing page and holiday view
from cal.views import Holiday, home
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
# Views to manage activities and events
from events.views import (
    activities,
    activities_list,
    activity_add,
    activity_edit,
    activity_delete,
    activity_search,
    events,
    events_list,
    event_add,
    event_edit,
    event_delete,
    event_multi_delete,
    event_permanent_removal,
    event_to_confirm,
    event_refused,
    # event_search,
)

urlpatterns = [
    path('', home, name="home"),
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
    # Activities URLs
    path('activities/', activities, name="activities"),
    path('htmx/activities-list/', activities_list, name="activities_list"),
    path('htmx/activity-add/', activity_add, name="activity_add"),
    path('htmx/activity/<pk>/edit/', activity_edit, name="activity_edit"),
    path('htmx/activity/<pk>/delete/', activity_delete, name="activity_delete"),
    path('htmx/activity-search/', activity_search, name="activity_search"),
    # Events URLs
    path('events/', events, name='events'),
    path('htmx/events_list/', events_list, name="events_list"),
    path('htmx/event-add/', event_add, name="event_add"),
    path('htmx/event/<pk>/edit/', event_edit, name="event_edit"),
    path('htmx/event/<pk>/delete/', event_delete, name="event_delete"),
    path('htmx/event-multi-delete/', event_multi_delete, name="event_multi_delete"),
    path('event-permanent-removal/', event_permanent_removal, name="event_permanent_removal"),
    path('event/to-confirm/<pk>/', event_to_confirm, name="event_to_confirm"),
    path('event/refused/<pk>/', event_refused, name="event_refused"),
    # path('htmx/event-search/', event_search, name="event_search"),
    # Django backend
    path('mgmt/', admin.site.urls),
]
