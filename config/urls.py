from django.contrib import admin
from django.urls import path

from cal.views import Home, Holiday
from accounts.views import register, Activate

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('holiday/<int:year>/<str:region>/', Holiday.as_view(), name="holiday"),
    path('register/', register, name="register"),
    path('activate/<uidb64>/<token>/', Activate.as_view(), name='activate'),
    path('mgmt/', admin.site.urls),
]
