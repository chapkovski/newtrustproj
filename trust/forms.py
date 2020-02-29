import django.forms as forms
from .models import Player, SenderDecision, SenderBelief, ReturnerBelief, ReturnDecision, return_choices
from django.forms import inlineformset_factory
from otree.api import widgets

from django.forms import BaseInlineFormSet

a = [1, 2, 3]
print('JOPA', list(zip(a, a, )))


class SenderForm(forms.ModelForm):
    CHOICES = ((True, 'Yes',), (False, 'No',))
    send = forms.ChoiceField(widget=widgets.RadioSelectHorizontal(attrs={'required': True}), choices=CHOICES,
                             required=True)


class ReturnForm(forms.ModelForm):
    CHOICES = list(zip(return_choices(), return_choices()))
    send_back = forms.ChoiceField(widget=widgets.RadioSelectHorizontal(attrs={'required': True}), choices=CHOICES,
                                  required=True)


class ReturnerBeliefForm(forms.ModelForm):
    CHOICES = ((True, 'Yes',), (False, 'No',))
    belief_on_send = forms.ChoiceField(widget=widgets.RadioSelectHorizontal(attrs={'required': True}), choices=CHOICES,
                                       required=True)


class SenderBeliefForm(forms.ModelForm):
    CHOICES = list(zip(return_choices(), return_choices()))
    belief_on_return = forms.ChoiceField(widget=widgets.RadioSelectHorizontal(attrs={'required': True}),
                                         choices=CHOICES,
                                         required=True)


def get_player_formset(model, fields, form=forms.ModelForm):
    return inlineformset_factory(parent_model=Player,
                                 model=model,
                                 fields=fields,
                                 extra=0,
                                 can_delete=False,
                                 form=form
                                 )


sender_formset = get_player_formset(SenderDecision, ['send'], SenderForm)
senderbelief_formset = get_player_formset(SenderBelief, ['belief_on_return'], SenderBeliefForm)
return_formset = get_player_formset(ReturnDecision, ['send_back'], ReturnForm)
returnbelief_formset = get_player_formset(ReturnerBelief, ['belief_on_send'], ReturnerBeliefForm)
