from django.contrib import admin

# Register your models here.
from apps.sample.models import Question, Option


class OptionInline(admin.TabularInline):
    model = Option
    extra = 1
    exclude = ['polling']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    view_on_site = True
    list_display = [
        "id",
        'question',
    ]
    inlines = [
        OptionInline
    ]
    search_fields = ['question']


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        'option',
    ]
    # exclude = ['polling']
    # fields = (
    #     'option', 'order',
    #     ('question', 'polling')
    # )
    search_fields = ['question']
    autocomplete_fields = ['question', 'polling']
    prepopulated_fields = {"option": ("order",)}

