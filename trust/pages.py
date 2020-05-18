from otree.api import Currency as c, currency_range
from typing import Union, List, Any, Optional
from ._builtin import WaitPage
from questionnaire.generic_pages import Page
from .generic_pages import ReturnerPage, SenderPage, FormSetMixin, CQPage, BlockerPage
from .models import City
from .forms import (sender_formset, return_formset, returnbelief_formset, senderbelief_formset,
                    averagereturnbelief_formset, averagesendbelief_formset)


class Instructions1(Page):
    show_instructions = False


class Instructions2(Page):
    show_instructions = True
    show_map = False


class SenderDecisionP(FormSetMixin, SenderPage, ):
    formset = sender_formset
    decision_type = 'sender_decision'
    show_instructions = True
    show_map = True
    show_block = 2


class ReturnDecisionP(FormSetMixin, ReturnerPage):
    formset = return_formset
    decision_type = 'return_decision'
    show_instructions = True
    show_map = True
    show_block = 3


class SenderBeliefP(FormSetMixin, SenderPage):
    formset = senderbelief_formset
    decision_type = 'sender_belief'
    show_instructions = True
    show_map = True


class ReturnerBeliefP(FormSetMixin, ReturnerPage):
    formset = returnbelief_formset
    decision_type = 'receiver_belief'
    show_instructions = True
    show_map = True


########### BLOCK: Comprehension questions ##############################################################
class CQ1(CQPage):
    page = 1
    show_instructions = True
    show_map = False


class CQ2(CQPage):
    page = 2
    show_instructions = True
    show_map = False


############ END OF: Comprehension questions #############################################################


########### BLOCK: AVERAGES ##############################################################
class Average2(FormSetMixin, Page):
    formset = averagesendbelief_formset
    decision_type = 'average_on_send_belief'
    show_instructions = True
    show_map = False


class Average3(FormSetMixin, Page):
    formset = averagereturnbelief_formset
    decision_type = 'average_on_return_belief'
    show_instructions = True
    show_map = False


############ END OF: AVERAGES #############################################################

########### BLOCK: INTROPATES ##############################################################
class IntroStage1(Page):
    pass


class ShowMap(Page):
    show_instructions = True
    show_map = True
    def vars_for_template(self):
        return dict(cities=City.objects.all().values('description'))


class AfterStage1(Page):
    pass


class InstructionsStage2(Page):
    pass


class IntroStage2(Page):
    pass


############ END OF: INTROPATES #############################################################


page_sequence = [
    # Instructions1,
    # Instructions2,
    # CQ1,
    ShowMap,
    # IntroStage1,
    # SenderDecisionP,
    # ReturnDecisionP,
    # AfterStage1,
    # InstructionsStage2,
    # CQ2,
    # IntroStage2,
    # SenderBeliefP,
    # ReturnerBeliefP,
    # Average2,
    # Average3,
]
