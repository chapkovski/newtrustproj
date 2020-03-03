from otree.api import Currency as c, currency_range
from typing import Union, List, Any, Optional
from ._builtin import Page, WaitPage
from .generic_pages import ReturnerPage, SenderPage, FormSetMixin, CQPage, BlockerPage
import random
from .forms import (sender_formset, return_formset, returnbelief_formset, senderbelief_formset,
                    averagereturnbelief_formset, averagesendbelief_formset)


class StartWP(WaitPage):
    group_by_arrival_time = True

    def is_displayed(self) -> bool:
        self.participant.vars.setdefault('matched', False)
        return True

    def get_players_for_group(self, waiting_players) -> Optional[list]:
        unmatched = [p for p in self.session.get_participants() if p.vars.get('matched') is None]
        if len(unmatched) < 2 and len(waiting_players) > 1: return waiting_players[:2]
        city1, city2 = self.subsession.cities
        city1players = [p for p in waiting_players if p.participant.vars.get('city') == city1]
        city2players = [p for p in waiting_players if p.participant.vars.get('city') == city2]
        if self.subsession.matched_different:
            if len(city1players) > 0 and len(city2players) > 0:
                self.subsession.matched_different = False
                candidates = [city1players[0], city2players[0]]
                random.shuffle(candidates)
                return candidates
        else:
            if len(city1players) > 1:
                self.subsession.matched_different = True
                return city1players[:2]
            if len(city2players) > 1:
                self.subsession.matched_different = True
                return city2players[:2]

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            roles = {1: 'Sender', 2: 'Receiver'}
            p.city = p.participant.vars.get('city')
            p.partner_city = p.other.participant.vars.get('city')
            p._role = roles[p.id_in_group]
            p.participant.vars['matched'] = True
            p.create_decisions()
            p.create_beliefs()
            p.create_averages()
class ConfirmationInstructions(Page):
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

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


########### BLOCK: Comprehension questions ##############################################################
class CQ1(CQPage):
    page = 1


class CQ2(CQPage):
    page = 2


############ END OF: Comprehension questions #############################################################


########### BLOCK: STOPPERS ##############################################################
class CQ1Blocker(BlockerPage):
    pass

class Stage1Blocker(BlockerPage):
    pass

class CQ1Blocker(BlockerPage):
    def is_displayed(self) -> bool:
        return self.session.config.get('cq', False)

class CQ2Blocker(BlockerPage):
    def is_displayed(self) -> bool:
        return self.session.config.get('cq', False)


class Stage2Blocker(BlockerPage):
    pass

class QuestionnaireBlocker(BlockerPage):
    pass





############ END OF: STOPPERS #############################################################

########### BLOCK: AVERAGES ##############################################################
class Average2(FormSetMixin, Page):
    formset = averagesendbelief_formset
    decision_type = 'average_on_send_belief'

class Average3(FormSetMixin, Page):
    formset = averagereturnbelief_formset
    decision_type = 'average_on_return_belief'

############ END OF: AVERAGES #############################################################


page_sequence = [
    StartWP,
    ConfirmationInstructions,
    CQ1Blocker,
    CQ1,
    Stage1Blocker,
    SenderDecisionP,
    ReturnDecisionP,
    CQ2Blocker,
    CQ2,
    Stage2Blocker,
    SenderBeliefP,
    ReturnerBeliefP,
    Average2,
    Average3,
    ResultsWaitPage,
    QuestionnaireBlocker,
]
