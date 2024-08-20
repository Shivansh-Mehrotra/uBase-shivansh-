from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from core.apps.permission.models import UserModuleAction

User = get_user_model()



# Register your models here.
class ModuleActionInline(admin.TabularInline):
    model = UserModuleAction
    verbose_name = 'Module Action'
    verbose_name_plural = 'Module Actions'
    extra = 1
    exclude = ('description',)
    # filter_horizontal = ['permissions']
    autocomplete_fields = ['module_action']


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'roles',),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('groups', 'user_permissions', 'roles')
    inlines = [
        ModuleActionInline
    ]
