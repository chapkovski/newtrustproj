from django.contrib import admin
from django.apps import apps
from otree.models import Participant, Session
from .models import UpdParticipant, TolokaParticipant


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
