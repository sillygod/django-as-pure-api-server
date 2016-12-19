from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.utils.translation import ugettext, ugettext_lazy as _

from .models import (
    User,
    Profile
)


class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'mobile_phone', )}),
        (_('permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'token', 'mobile_phone', 'email', 'first_name', 'last_name', 'is_staff', 'last_login')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'token')


admin.site.register(User, UserAdmin)
