from django.contrib import admin
from core.models import Tutorial, Step, Inst, OurUser


class StepInline(admin.TabularInline):
    model = Step


class TutorialAdmin(admin.ModelAdmin):
    inlines = [
        StepInline,
    ]


class OurUserAdmin(admin.ModelAdmin):
    model = OurUser


class InstAdmin(admin.ModelAdmin):
    model = Inst


admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(Inst, InstAdmin)
admin.site.register(OurUser, OurUserAdmin)
