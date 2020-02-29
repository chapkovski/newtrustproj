import django.forms as forms
from .models import Player, SenderDecision, SenderBelief, ReturnerBelief, ReturnDecision, return_choices, Constants
from django.forms import inlineformset_factory
from otree.api import widgets


class SenderForm(forms.ModelForm):
    CHOICES = Constants.sender_choices
    send = forms.ChoiceField(widget=widgets.RadioSelectHorizontal(attrs={'required': True}), choices=CHOICES,
                             required=True)


class ReturnForm(forms.ModelForm):
    CHOICES = Constants.expanded_receiver_choices
    send_back = forms.ChoiceField(widget=widgets.RadioSelectHorizontal(attrs={'required': True}), choices=CHOICES,
                                  required=True)


class ReturnerBeliefForm(forms.ModelForm):
    CHOICES = Constants.sender_choices
    belief_on_send = forms.ChoiceField(widget=widgets.RadioSelectHorizontal(attrs={'required': True}), choices=CHOICES,
                                       required=True)


class SenderBeliefForm(forms.ModelForm):
    CHOICES = Constants.expanded_receiver_choices
    belief_on_return = forms.ChoiceField(widget=widgets.RadioSelectHorizontal(attrs={'required': True}),
                                         choices=CHOICES,
                                         required=True)


class SorterFormset(forms.BaseInlineFormSet):
    def get_queryset(self):
        initial_q = super().get_queryset()
        asc_order = '' if self.instance.participant.vars.get('city_order') else '-'
        return initial_q.order_by(f'{asc_order}city__description')


def get_player_formset(model, fields, form=forms.ModelForm):
    return inlineformset_factory(parent_model=Player,
                                 model=model,
                                 formset=SorterFormset,
                                 fields=fields,
                                 extra=0,
                                 can_delete=False,
                                 form=form
                                 )


sender_formset = get_player_formset(SenderDecision, ['send'], SenderForm)
senderbelief_formset = get_player_formset(SenderBelief, ['belief_on_return'], SenderBeliefForm)
return_formset = get_player_formset(ReturnDecision, ['send_back'], ReturnForm)
returnbelief_formset = get_player_formset(ReturnerBelief, ['belief_on_send'], ReturnerBeliefForm)
