from django.contrib import admin

from core.apps.lookup_management.models import LookupType, Lookup


class LookupInline(admin.TabularInline):
    model = Lookup
    extra = 3
    exclude = ['polling']


# Register your models here.
@admin.register(LookupType)
class LookupTypeAdmin(admin.ModelAdmin):
    view_on_site = True
    list_display = [
        "name", "key", "parent",
    ]
    inlines = [
        LookupInline
    ]
    fieldsets = (
        (None, {'fields': ("name", "key", "parent",)}),
        (None, {'fields': ("is_active", "is_deleted",)}),

    )
    # search_fields = ['question']