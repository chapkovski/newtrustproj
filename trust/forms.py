import django.forms as forms
from .models import Player, Decision, Constants, CQ
from django.forms import inlineformset_factory, BaseModelFormSet, BaseInlineFormSet
from otree.api import widgets
from django.db.models import Max

DEFAULT_ERRMSG_FALLBACK = 'Проверьте правильность ваших ответов'


class SelfCleaningMixin:
    def __init__(self, zeroing=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.zeroing = zeroing

    def render(self, name, value, *args, **kwargs):
        if self.zeroing:
            value = None
        return super().render(name, value, *args, **kwargs)


class SelfCleaningNumber(SelfCleaningMixin, forms.NumberInput):
    pass


class SelfCleaningChoice(SelfCleaningMixin, widgets.RadioSelect):
    def __init__(self, *args, **kwargs):
        cleaned_choices = [i for i, j in kwargs['choices']]
        self.enabled = kwargs.pop('enabled', cleaned_choices)
        super().__init__(*args, **kwargs)

    def create_option(self, name, value, *args, **kwargs):
        options = super().create_option(name, value, *args, **kwargs)
        options['attrs']['disabled'] = not (value in self.enabled)
        return options


class CQForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        zeroing = False
        extra_attrs = dict(required=True)
        fix_choice = False
        if kwargs.get('data') and not self.is_valid():
            zeroing = True

            if self.instance.counter > Constants.max_cq_attempts:
                coranswer = self.instance.correct_answer
                extra_attrs = dict(**extra_attrs, max=coranswer, min=coranswer)
                fix_choice = [coranswer]
        params = dict(zeroing=zeroing,
                      attrs=extra_attrs)
        if self.instance.choices:
            widget = SelfCleaningChoice
            cleaned_choices = [i for i, j in self.instance.choices]
            if fix_choice:
                enabled = [self.instance.correct_answer]
            else:
                enabled = cleaned_choices
            params = dict(**params, choices=self.instance.choices, enabled=enabled)
        else:
            widget = SelfCleaningNumber

        if kwargs.get('data') and self.is_valid():
            widget = forms.HiddenInput
            params = {}
        self.fields['answer'] = forms.IntegerField(
            label=self.instance.text,
            widget=widget(**params),
            required=True
        )
        self.fields['answer'].extid = self.instance.extid

    def clean_answer(self):
        q = self.instance
        answer = self.cleaned_data.get('answer')
        if q.counter > Constants.max_cq_attempts:
            return answer
        if answer != q.correct_answer:
            wrong_answer = q.wrong_answer
            q.counter += 1
            q.save()
            raise forms.ValidationError(wrong_answer)
        return answer


class CQFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.part = kwargs.pop('part')
        super().__init__(*args, **kwargs)

    def clean(self):
        if any(self.errors):
            mcounter = (self.queryset.aggregate(mcounter=Max('counter')))['mcounter']
            error_part = Constants.error_msg_parts.get(self.part, '')

            general_msg = Constants.general_error_msg.get(mcounter, DEFAULT_ERRMSG_FALLBACK).format(error_part)
            if general_msg:
                raise forms.ValidationError(general_msg)


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
                                   form=CQForm,
                                   formset=CQFormSet
                                   )
