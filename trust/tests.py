from otree.api import Currency as c, currency_range, SubmissionMustFail
from .pages import *
from ._builtin import Bot
from .models import Constants

import random


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

    def play_round(self):
        yield Instructions1
        yield Instructions2
        if self.session.config.get('cq'):

            сc1answers = dict(
                cq1_1=30,
                cq1_2=30,
                cq1_3=21,
                cq1_4=31,
                cq1_5=9,
                cq1_6=10,
                cq1_7=10,
                cq1_8=3,
                cq1_9=2,
            )
            cq1wronganswers = {k: v + 1 for k, v in сc1answers.items()}
            # yield SubmissionMustFail(CQ1, cq1wronganswers)
            yield CQ1, сc1answers
            cq2answers = dict(
                cq2_1=0,
                cq2_2=10,
                cq2_3=0,
                cq2_4=10,
                cq2_5=0,
            )
            cq2wronganswers = {k: v + 1 for k, v in cq2answers.items()}

        if self.player.role() == 'Sender':
            yield SenderDecisionP, self._create_data(name='senderdecisions', field_name='answer',
                                                     choice_set=[0, Constants.endowment])
            if self.session.config.get('cq'):

                # yield SubmissionMustFail(CQ2, cq2wronganswers)
                yield CQ2, cq2answers

            yield SenderBeliefP, self._create_data(name='senderbeliefs', field_name='belief_on_return',
                                                   choice_set=Constants.receiver_choices)
        else:
            yield ReturnDecisionP, self._create_data(name='returndecisions', field_name='send_back',
                                                     choice_set=Constants.receiver_choices)

            if self.session.config.get('cq'):

                # yield SubmissionMustFail(CQ2,cq2wronganswers)
                yield CQ2, cq2answers

            yield ReturnerBeliefP, self._create_data(name='returnerbeliefs', field_name='belief_on_send',
                                                     choice_set=[0, Constants.endowment])

        average1_answer = (
            {'sender_confident_return': random.choice(
                Constants.receiver_choices)} if self.player.role() == 'Sender' else {
                'receiver_confident_send': random.choice(
                    [0, Constants.endowment])})
        yield Average2, self._create_data(name='averageonsendbeliefs', field_name='average_belief_on_send',
                                          choice_set=range(0, 100))
        yield Average3, self._create_data(name='averageonreturnbeliefs', field_name='average_belief_on_return',
                                          choice_set=Constants.receiver_choices)

