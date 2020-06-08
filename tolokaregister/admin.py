from django.contrib import admin
from django.apps import apps
from otree.models import Participant, Session
from .models import UpdParticipant, TolokaParticipant


@admin.register(Participant)
class PPAdmin(admin.ModelAdmin):
    def get_session_code(self, obj):
        return obj.session.code
    list_display = ('code', 'get_session_code', 'id_in_session')
    exclude = ['vars']

@admin.register(UpdParticipant)
class PAdmin(admin.ModelAdmin):
    fields = ['label', 'payoff']



@admin.register(TolokaParticipant)
class TAdmin(admin.ModelAdmin):
    pass


models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
