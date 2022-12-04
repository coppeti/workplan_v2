from django.contrib import admin
from django.urls import path

from cal.views import Home, Holiday
from accounts.views import signup

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('holiday/<int:year>/<str:region>/', Holiday.as_view(), name="holiday"),
    path('signup/', signup, name="signup"),
    path('mgmt/', admin.site.urls),
]
