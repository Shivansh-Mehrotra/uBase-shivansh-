from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from rest_framework.reverse import reverse

from core.apps.permission.models import Module, ModuleAction, RoleModuleAction
from core.apps.role.models import AppSource, Role


@admin.register(AppSource)
class AppSourceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        'label',
        'source_key',
        'description',
    ]


class RoleModuleActionInline(admin.TabularInline):
    model = RoleModuleAction
    extra = 1
    autocomplete_fields = ['module_action']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    filter_horizontal = ['permissions', 'module_actions']
    inlines = [
        RoleModuleActionInline
    ]
    list_display = (
        'id', 'name', 'key', 'app_source_link'
    )
    list_filter = ['app_source']
    autocomplete_fields = ['default_module_action']

    def app_source_link(self, obj):
        if not obj.app_source:
            return '-'
        url = reverse("admin:role_appsource_change", args=[obj.app_source.id])
        link = '<a href="%s">%s</a>' % (url, obj.app_source)
        return mark_safe(link)
    app_source_link.short_description = 'App Source'

