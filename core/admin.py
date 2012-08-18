from django.contrib import admin
from core.models import Tutorial, Step, Instance


class StepInline(admin.TabularInline):
    model = Step


class TutorialAdmin(admin.ModelAdmin):
    inlines = [
        StepInline,
    ]


class InstanceAdmin(admin.ModelAdmin):
    model = Instance


admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(Instance, InstanceAdmin)
