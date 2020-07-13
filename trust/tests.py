from otree.api import Currency as c, currency_range, SubmissionMustFail
from .pages import *
from ._builtin import Bot
from .models import Constants

import random


class PseudoPage:
    def __init__(self, player, part):
        self.player = player
        self.part = part


class PlayerBot(Bot):
    def _create_data(self, name, field_name, choice_set):
        senderdecisions = getattr(self.player, name).all()
        ids = senderdecisions.values_list('id', flat=True)
        name = 'decisions'
        field_name = 'answer'
        ids_dct = dict()
        pls_dct = dict()
        for i, j in enumerate(ids):
            ids_dct[f'{name}-{i}-id'] = j
            pls_dct[f'{name}-{i}-owner'] = self.player.pk
        nbundles = senderdecisions.count()

        answers_dct = dict()
        for i, j in enumerate(ids):
            answers_dct[f'{name}-{i}-{field_name}'] = random.choice(choice_set)

        return {
            f'{name}-TOTAL_FORMS': nbundles,
            f'{name}-INITIAL_FORMS': nbundles,
            f'{name}-MIN_NUM_FORMS': '0',
            f'{name}-MAX_NUM_FORMS': '1000',
            **answers_dct,
            **ids_dct,
            **pls_dct,
        }

    def _cq_data(self, page_obj):
        pseudo = PseudoPage(player=self.player, part=page_obj.part)
        q = page_obj.get_cq_instances(pseudo)
        name = 'cqs'
        field_name = 'answer'
        full_answers = {}
        for i, j in enumerate(q):
            full_answers[f'{name}-{i}-id'] = j.id
            full_answers[f'{name}-{i}-owner'] = self.player.pk
            full_answers[f'{name}-{i}-{field_name}'] = j.correct_answer
        return {
            f'{name}-TOTAL_FORMS': q.count(),
            f'{name}-INITIAL_FORMS': q.count(),
            f'{name}-MIN_NUM_FORMS': '0',
            f'{name}-MAX_NUM_FORMS': '1000',
            **full_answers
        }

    def play_round(self):
        yield Instructions1
        yield Instructions2
        yield CQ1, self._cq_data(CQ1)
        yield IntroStage1,
        yield ShowMap,
        if self.player.role() == 'sender':
            yield SenderDecisionP, self._create_data(name='senderdecisions', field_name='answer',
                                                     choice_set=[0, Constants.endowment])
            yield AfterStage1
            yield InstructionsStage2
            yield ExamplesStage2
            yield CQ2, self._cq_data(CQ2)
            yield IntroStage2
            yield SenderBeliefP, self._create_data(name='senderbeliefs', field_name='belief_on_return',
                                                   choice_set=Constants.receiver_choices)
        else:
            yield ReturnDecisionP, self._create_data(name='returndecisions', field_name='send_back',
                                                     choice_set=Constants.receiver_choices)
            yield AfterStage1
            yield InstructionsStage2
            yield ExamplesStage2

            yield CQ2, self._cq_data(CQ2)

            yield IntroStage2
            yield ReturnerBeliefP, self._create_data(name='returnerbeliefs', field_name='belief_on_send',
                                                     choice_set=[0, Constants.endowment])


        yield Average2, self._create_data(name='averageonsendbeliefs', field_name='average_belief_on_send',
                                          choice_set=range(0, 100))
        yield Average3, self._create_data(name='averageonreturnbeliefs', field_name='average_belief_on_return',
                                          choice_set=Constants.receiver_choices)

