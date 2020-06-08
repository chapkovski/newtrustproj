import django.forms as forms
from .models import Player, Decision, Constants
from django.forms import inlineformset_factory




class SorterFormset(forms.BaseInlineFormSet):
    model = Decision

    def __init__(self, decision_type, *args, **kwargs):
        self.decision_type = decision_type
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        initial_q = self.model.objects.filter(decision_type=self.decision_type, owner=self.instance)
        asc_order = '' if self.instance.participant.vars.get('city_order') else '-'
        return initial_q.order_by(f'{asc_order}city__description')


def get_player_formset( form=forms.ModelForm):
    return inlineformset_factory(parent_model=Player,
                                 model=Decision,
                                 formset=SorterFormset,
                                 fields=['answer'],
                                 extra=0,
                                 can_delete=False,
                                 form=form
                                 )


