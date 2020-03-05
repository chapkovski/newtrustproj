from django.contrib import admin

# Register your models here.
from django.apps import apps
from .models import Decision

from import_export import resources


class DecisionResource(resources.ModelResource):
    class Meta:
        model = Decision
        fields = ('owner__id', 'owner__session__code', 'owner__participant__code', 'owner__city', 'decision_type',
                  'city__code', 'city__description', 'answer',)


from import_export.admin import ImportExportModelAdmin


class DecisionAdmin(ImportExportModelAdmin):
    resource_class = DecisionResource


admin.site.register(Decision, DecisionAdmin)
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
