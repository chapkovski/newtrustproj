from import_export import resources
from .models import Decision

class DecisionResource(resources.ModelResource):
    class Meta:
        model = Decision
        fields = ('owner__session__code','owner__participant__code','owner___role', 'decision_type',
                  'owner__city','city__description', 'city__code', 'answer')