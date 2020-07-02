import django.forms as forms
from .models import Player, Decision, Constants, CQ
from django.forms import inlineformset_factory
from otree.api import widgets


class CQForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.choices:
            widget = widgets.RadioSelect(choices=self.instance.choices)
        else:
            widget = forms.NumberInput()

        self.fields['answer'] = forms.IntegerField(
            label=self.instance.text,
            widget=widget
        )

    def clean_answer(self):
        q = self.instance
        answer = self.cleaned_data.get('answer')
        if q.counter > Constants.max_cq_attempts:
            return answer
        if answer != q.correct_answer:
            q.counter += 1
            q.save()
            raise forms.ValidationError(q.wrong_answer)
        return answer


class SenderForm(forms.ModelForm):
    CHOICES = Constants.sender_choices
    answer = forms.ChoiceField(widget=widgets.RadioSelectHorizontal(attrs={'required': True}), choices=CHOICES,
                               required=True)


class ReturnForm(forms.ModelForm):
    CHOICES = Constants.expanded_receiver_choices
    answer = forms.ChoiceField(widget=widgets.RadioSelectHorizontal(attrs={'required': True}), choices=CHOICES,
                               required=True)


class ReturnerBeliefForm(forms.ModelForm):
    CHOICES = Constants.sender_choices
    answer = forms.ChoiceField(widget=widgets.RadioSelectHorizontal(attrs={'required': True}), choices=CHOICES,
                               required=True)


class SenderBeliefForm(forms.ModelForm):
    CHOICES = Constants.expanded_receiver_choices
    answer = forms.ChoiceField(widget=widgets.RadioSelectHorizontal(attrs={'required': True}),
                               choices=CHOICES,
                               required=True)


class AverageOnReturnBeliefForm(forms.ModelForm):
    answer = forms.IntegerField(widget=forms.NumberInput(attrs={'required': True}),
                                min_value=0,
                                max_value=Constants.endowment * Constants.coef,
                                required=True)


class AverageOnSendBeliefForm(forms.ModelForm):
    answer = forms.IntegerField(widget=forms.NumberInput(attrs={'required': True}),
                                min_value=0,
                                max_value=100,
                                required=True)


class SorterFormset(forms.BaseInlineFormSet):
    model = Decision

    def __init__(self, decision_type, *args, **kwargs):
        self.decision_type = decision_type
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        initial_q = self.model.objects.filter(decision_type=self.decision_type, owner=self.instance)
        asc_order = '' if self.instance.participant.vars.get('city_order') else '-'
        return initial_q.order_by(f'{asc_order}city__description')


def get_player_formset(form=forms.ModelForm):
    return inlineformset_factory(parent_model=Player,
                                 model=Decision,
                                 formset=SorterFormset,
                                 fields=['answer'],
                                 extra=0,
                                 can_delete=False,
                                 form=form
                                 )


sender_formset = get_player_formset(SenderForm)
senderbelief_formset = get_player_formset(SenderBeliefForm)
return_formset = get_player_formset(ReturnForm)
returnbelief_formset = get_player_formset(ReturnerBeliefForm)
averagesendbelief_formset = get_player_formset(AverageOnSendBeliefForm)
averagereturnbelief_formset = get_player_formset(AverageOnReturnBeliefForm)

# formset for cqs
cq_formset = inlineformset_factory(parent_model=Player,
                                   model=CQ,
                                   fields=['answer'],
                                   extra=0,
                                   can_delete=False,
                                   form=CQForm
                                   )
