from otree.api import Currency as c, currency_range
from typing import Union, List, Any, Optional
from ._builtin import Page, WaitPage
from .generic_pages import ReturnerPage, SenderPage, FormSetMixin
import random
from .forms import sender_formset, return_formset, returnbelief_formset, senderbelief_formset


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
            p.city = p.participant.vars.get('city')
            p._role = p.role()  # just to store it in db;
            p.participant.vars['matched'] = True
            p.create_decisions()
            p.create_beliefs()


class SenderDecisionP(FormSetMixin, SenderPage):
    formset = sender_formset



class ReturnDecisionP(FormSetMixin, ReturnerPage):
    formset = return_formset


class SenderBeliefP(FormSetMixin, SenderPage):
    formset = senderbelief_formset


class ReturnerBeliefP(FormSetMixin, ReturnerPage):
    formset = returnbelief_formset


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    StartWP,
    SenderDecisionP,
    ReturnDecisionP,
    SenderBeliefP,
    ReturnerBeliefP,
    ResultsWaitPage,
    Results

]
