from django.contrib import admin
from core.models import Tutorial, Step


class StepInline(admin.TabularInline):
    model = Step

class TutorialAdmin(admin.ModelAdmin):
    inlines = [
        StepInline,
    ]

admin.site.register(Tutorial, TutorialAdmin)