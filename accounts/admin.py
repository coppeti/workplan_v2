from django.contrib import admin
from accounts.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_active')
    exclude = ('password', 'last_login',)
    fields = ('first_name', 'last_name', 'username', 'email', 'birthday',)


admin.site.register(User, UserAdmin)
    