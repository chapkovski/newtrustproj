from django.contrib import admin
from django.apps import apps
from otree.models import Participant, Session
from .models import UpdParticipant, TolokaParticipant


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('code', 'num_participants', 'label','is_demo')
    list_display_links = ['code']
    readonly_fields = ['vars', 'config',
                       '_admin_report_app_names',
                       '_admin_report_num_rounds',
                       'mturk_expiration',
                       'mturk_qual_id']


@admin.register(Participant)
class PPAdmin(admin.ModelAdmin):
    def get_session_code(self, obj):
        return obj.session.code

    list_display = ('code', 'get_session_code', 'id_in_session')
    readonly_fields = ['vars', 'label', 'mturk_assignment_id', 'mturk_worker_id', '_waiting_for_ids',
                       '_current_form_page_url', '_timeout_expiration_time']


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
