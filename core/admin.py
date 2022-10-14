from django.contrib import admin
from .models import Intents, Questions, Intent_Answers, Variables


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('intents', 'question')


class IntentAnswersAdmin(admin.ModelAdmin):
    list_display = ('intent', 'EN_Answer', 'FR_Answer')


# Register your models here.
admin.site.register(Intents)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Intent_Answers, IntentAnswersAdmin)
admin.site.register(Variables)

