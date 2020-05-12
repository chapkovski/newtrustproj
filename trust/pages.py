from otree.api import Currency as c, currency_range
from typing import Union, List, Any, Optional
from ._builtin import WaitPage
from questionnaire.generic_pages import Page
from .generic_pages import ReturnerPage, SenderPage, FormSetMixin, CQPage, BlockerPage

from .forms import (sender_formset, return_formset, returnbelief_formset, senderbelief_formset,
                    averagereturnbelief_formset, averagesendbelief_formset)


class Instructions1(Page):
    pass

class Instructions2(Page):
    pass


class SenderDecisionP(FormSetMixin, SenderPage, ):
    formset = sender_formset
    decision_type = 'sender_decision'


class ReturnDecisionP(FormSetMixin, ReturnerPage):
    formset = return_formset
    decision_type = 'return_decision'


class SenderBeliefP(FormSetMixin, SenderPage):
    formset = senderbelief_formset
    decision_type = 'sender_belief'


class ReturnerBeliefP(FormSetMixin, ReturnerPage):
    formset = returnbelief_formset
    decision_type = 'receiver_belief'



########### BLOCK: Comprehension questions ##############################################################
class CQ1(CQPage):
    page = 1


class CQ2(CQPage):
    page = 2


############ END OF: Comprehension questions #############################################################


########### BLOCK: AVERAGES ##############################################################
class Average2(FormSetMixin, Page):
    formset = averagesendbelief_formset
    decision_type = 'average_on_send_belief'


class Average3(FormSetMixin, Page):
    formset = averagereturnbelief_formset
    decision_type = 'average_on_return_belief'

############ END OF: AVERAGES #############################################################


page_sequence = [
    Instructions1,
    Instructions2,
    CQ1,
    SenderDecisionP,
    ReturnDecisionP,
    CQ2,
    SenderBeliefP,
    ReturnerBeliefP,
    Average2,
    Average3,
]
