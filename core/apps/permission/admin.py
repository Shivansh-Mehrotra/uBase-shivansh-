from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Permission
from django.utils.safestring import mark_safe
from rest_framework.reverse import reverse

from core.apps.permission.models import Module, ModuleAction, RoleModuleAction


class ModuleActionInline(admin.StackedInline):
    model = ModuleAction
    verbose_name = 'Module Action'
    verbose_name_plural = 'Module Actions'
    extra = 1
    exclude = ('description',)
    filter_horizontal = ['permissions']


class ModuleInline(admin.TabularInline):
    model = Module
    verbose_name = 'Child Module'
    verbose_name_plural = 'Child Modules'
    extra = 1
    exclude = ('description',)
    inlines = [
        ModuleActionInline
    ]


@admin.register(Module)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'module_key',
        'label',
        'parent_link',
        'app_source_link',
        'order',
    )
    inlines = [ ModuleInline, ModuleActionInline, ]
    list_filter = ['app_source']
    search_fields = ('label', 'module_key')
    ordering = ['-parent', 'module_key']

    def parent_link(self, obj):
        if not obj.parent:
            return '-'
        url = reverse("admin:permission_module_change", args=[obj.parent.id])
        link = '<a href="%s">%s</a>' % (url, obj.parent)
        return mark_safe(link)
    parent_link .short_description = 'Parent Module'

    def app_source_link(self, obj):
        if not obj.app_source:
            return '-'
        url = reverse("admin:role_appsource_change", args=[obj.app_source.id])
        link = '<a href="%s">%s</a>' % (url, obj.app_source)
        return mark_safe(link)
    app_source_link.short_description = 'App Source'


# Module Action

class RoleModuleActionInline(admin.TabularInline):
    model = RoleModuleAction
    extra = 1
    autocomplete_fields = ['module_action']

@admin.register(ModuleAction)
class ModuleActionAdmin(admin.ModelAdmin):
    filter_horizontal = ['permissions', 'role']
    inlines = [RoleModuleActionInline]
    search_fields = (
        'action', 'label', 'description', 'route_url', 'module__module_key'
    )
    list_display = ['id', 'module_link', 'action', 'label', 'order', ]
    
    def module_link(self, obj):
        if not obj.module:
            return '-'
        url = reverse("admin:permission_module_change", args=[obj.module.id])
        link = '<a href="%s">%s</a>' % (url, obj.module)
        return mark_safe(link)
    module_link .short_description = 'Module'