from otree.api import Currency as c, currency_range
from typing import Union, List, Any, Optional
from ._builtin import WaitPage
from questionnaire.generic_pages import Page
from .generic_pages import ReturnerPage, SenderPage, FormSetMixin, CQPage
from .models import City
from .forms import (sender_formset, return_formset, returnbelief_formset, senderbelief_formset,
                    averagereturnbelief_formset, averagesendbelief_formset)


class FirstWP(WaitPage):
    group_by_arrival_time = True

    after_all_players_arrive = 'set_players_params'


class Instructions1(Page):
    show_instructions = False


class Instructions2(Page):
    show_instructions = True
    show_instructions_1 = True
    show_map = False


class SenderDecisionP(FormSetMixin, SenderPage, ):
    formset = sender_formset
    decision_type = 'sender_decision'
    show_instructions = True
    show_instructions_1 = True
    show_map = True
    show_block = 2


class ReturnDecisionP(FormSetMixin, ReturnerPage):
    formset = return_formset
    decision_type = 'return_decision'
    show_instructions = True
    show_instructions_1 = True
    show_map = True
    show_block = 3


class SenderBeliefP(FormSetMixin, SenderPage):
    formset = senderbelief_formset
    decision_type = 'sender_belief'
    show_instructions = True
    show_instructions_1 = True
    show_instructions_2 = True
    show_map = True


class ReturnerBeliefP(FormSetMixin, ReturnerPage):
    formset = returnbelief_formset
    decision_type = 'receiver_belief'
    show_instructions = True
    show_instructions_1 = True
    show_instructions_2 = True
    show_map = True


########### BLOCK: Comprehension questions ##############################################################
class CQ1(CQPage):
    part = 1
    show_instructions = True
    show_map = False
    show_instructions_1 = True


class CQ2(CQPage):
    part = 2
    show_instructions = True
    show_instructions_1 = True
    show_instructions_2 = True
    show_map = True


############ END OF: Comprehension questions #############################################################


########### BLOCK: AVERAGES ##############################################################
class Average2(FormSetMixin, Page):
    formset = averagesendbelief_formset
    decision_type = 'average_on_send_belief'
    show_instructions = True
    show_instructions_1 = True
    show_instructions_2 = True
    show_map = True


class Average3(FormSetMixin, Page):
    formset = averagereturnbelief_formset
    decision_type = 'average_on_return_belief'
    show_instructions = True
    show_instructions_1 = True
    show_instructions_2 = True
    show_map = True

    def before_next_page(self):
        """If a person has reached this stage that means we can use him for calculating payoffs of others.
        Theoretically it would be better to move this logic to toloka code provision, but let's ignore that for now"""
        self.player.calculable = True


############ END OF: AVERAGES #############################################################

########### BLOCK: INTROPATES ##############################################################
class IntroStage1(Page):
    show_instructions = True

    def before_next_page(self):
        self.player.assign_role()


class ShowMap(Page):
    show_instructions = True
    show_instructions_1 = True

    show_map = True

    def vars_for_template(self):
        return dict(cities=City.objects.all().values('description'))


class AfterStage1(Page):
    pass


class InstructionsStage2(Page):
    pass


class ExamplesStage2(Page):
    show_instructions = True
    show_instructions_1 = True
    show_instructions_2 = True
    show_map = True


class IntroStage2(Page):
    show_instructions = True
    show_instructions_1 = True
    show_instructions_2 = True
    show_map = True


############ END OF: INTROPATES #############################################################

class DebugQ(Page):
    form_model = 'player'
    form_fields = ['comment']
    def is_displayed(self):
        return self.session.config.get('debug', False)


page_sequence = [
    FirstWP,
    # Instructions1,
    # Instructions2,
    # CQ1,
    # IntroStage1,
    ShowMap,
    SenderDecisionP,
    ReturnDecisionP,
    AfterStage1,
    InstructionsStage2,
    ExamplesStage2,
    CQ2,
    IntroStage2,
    SenderBeliefP,
    ReturnerBeliefP,
    Average2,
    Average3,
    DebugQ,
]
