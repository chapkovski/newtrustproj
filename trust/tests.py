from otree.api import Currency as c, currency_range
from .pages import *
from ._builtin import Bot
from .models import Constants

import random


class PlayerBot(Bot):
    def _create_data(self, name, field_name, choice_set):
        senderdecisions = getattr(self.player, name).all()
        ids = senderdecisions.values_list('id', flat=True)
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
            f'{name}-MIN_NUM_FORMS': ['0'],
            f'{name}-MAX_NUM_FORMS': ['1000'],
            **answers_dct,
            **ids_dct,
            **pls_dct,
        }

    def play_round(self):
        pass
        if self.player.role() == 'Sender':
            yield SenderDecisionP, self._create_data(name='senderdecisions', field_name='send',
                                                     choice_set=[0, Constants.endowment])
            yield SenderBeliefP, self._create_data(name='senderbeliefs', field_name='belief_on_return',
                                                   choice_set=Constants.receiver_choices)
        else:
            yield ReturnDecisionP, self._create_data(name='returndecisions', field_name='send_back',
                                                     choice_set=Constants.receiver_choices)
            yield ReturnerBeliefP, self._create_data(name='returnerbeliefs', field_name='belief_on_send',
                                                     choice_set=[0, Constants.endowment])
        yield Results
