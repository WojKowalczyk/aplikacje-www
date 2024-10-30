from django.contrib import admin

from .models import Choice, Question, Osoba, Stanowisko


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ["question_text"]
    list_filter = ["pub_date"]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]


class OsobaAdmin(admin.ModelAdmin):
    readonly_fields = ["data_dodania"]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Osoba, OsobaAdmin)
admin.site.register(Stanowisko)