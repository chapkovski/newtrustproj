import pandas as pd
from trust.models import Decision
from questionnaire.models import Player as QPlayer
from trust.models import Player as TPlayer
from django.db.models import IntegerField, Count, Q
from django.db.models.functions import Cast
from otree.models_concrete import PageCompletion
from otree.models import Session
import logging

logger = logging.getLogger(__name__)


def renamer(oldname):
    newname = oldname.strip('_').replace('__', '_')
    return newname


def reshuffle_data(data):
    data.rename(renamer, axis='columns', inplace=True)
    data = data * 1
    data['role'] = data['role'].replace({'receiver': 1, 'sender': 0, }).fillna('')
    return data


class UniGetter:
    def __init__(self, obj, sessions):
        self.obj = obj
        self.sessions = sessions

    def get_queryset(self):
        return self.obj.objects.filter(session__in=self.sessions)

    def data_exists(self):
        return self.get_queryset().exists()

    def get_data(self):
        q = self.get_queryset()
        if q.exists():
            return self.process_data(data=q)

    def process_data(self, data):
        return


class TrustDataGetter(UniGetter):
    def process_data(self, data):
        toconv = ['_payoff',
                  'endowment',
                  'stage1payoff',
                  'stage2payoff',
                  ]
        curconverter = {}
        for p in toconv:
            curconverter[f'trustgame_{p}'] = Cast(p, output_field=IntegerField())
        cq_annotator = dict(
            cq0_stage1=Count('cqs__counter', filter=Q(cqs__part=1, cqs__counter=0)),
            cq1_stage1=Count('cqs__counter', filter=Q(cqs__part=1, cqs__counter=1)),
            cq2_stage1=Count('cqs__counter', filter=Q(cqs__part=1, cqs__counter=2)),
            cq3_stage1=Count('cqs__counter', filter=Q(cqs__part=1, cqs__counter=3)),
            cq0_stage2=Count('cqs__counter', filter=Q(cqs__part=2, cqs__counter=0)),
            cq1_stage2=Count('cqs__counter', filter=Q(cqs__part=2, cqs__counter=1)),
            cq2_stage2=Count('cqs__counter', filter=Q(cqs__part=2, cqs__counter=2)),
            cq3_stage2=Count('cqs__counter', filter=Q(cqs__part=2, cqs__counter=3)),

        )
        data = data.annotate(**curconverter, **cq_annotator).values()
        df = pd.DataFrame(list(
            data.values('session__code', 'participant__code', 'participant__time_started', 'city',
                        '_role', 'city_order', 'participant__id_in_session', 'participant__label',
                        'cq1_counter', 'cq2_counter',
                        *cq_annotator.keys(),
                        *curconverter.keys(),
                        )))
        df.set_index('participant__code', inplace=True)
        df['participant__time_started'] = pd.to_datetime(df['participant__time_started'], unit='s').dt.strftime(
            '%B %d, %Y, %r')
        return df


class DecisionGetter(UniGetter):
    def get_queryset(self):
        return self.obj.objects.filter(owner__session__in=self.sessions,
                                       answer__isnull=False)

    def process_data(self, data):
        df = pd.DataFrame(list(data.values('city__code', 'decision_type', 'owner__participant__code', 'answer')))
        df.rename(dict(owner__participant__code='participant__code'), axis='columns', inplace=True)

        table = pd.pivot_table(df, values='answer', index=['participant__code'],
                               columns=['decision_type', 'city__code'])
        table.columns = ['_'.join(col).strip() for col in table.columns.values]
        return table


class QGetter(UniGetter):
    def process_data(self, data):
        skip_fields = [
            '_payoff',
            '_id_in_subsession',
            'round_number',
            'id_in_group',
            '_gbat_arrived',
            '_gbat_grouped',
            'id',
            'participant',
            'session',
            'subsession',
            'group',
        ]

        fields = [q.name for q in self.obj._meta.get_fields() if q.name not in skip_fields]
        df = pd.DataFrame(list(data.values(*fields, 'participant__code', )))
        df.set_index('participant__code', inplace=True)
        return df


class TimeGetter(UniGetter):
    def get_queryset(self):
        q = super().get_queryset()
        pages = ['CQ1', 'CQ2', 'SenderDecisionP', 'SenderBeliefP', 'ReturnDecisionP', 'ReturnerBeliefP', 'Average2',
                 'Average3',
                 'Motivation', ]
        return q.filter(page_name__in=pages)

    def process_data(self, data):
        ps = data.values('participant__code', 'page_name', 'seconds_on_page')
        df = pd.DataFrame(list(ps))
        df['page_name'] = df['page_name'].apply(lambda x: f'time_{x}')
        table = pd.pivot_table(df, values='seconds_on_page', index=['participant__code'],
                               columns=['page_name'])

        return table


def get_full_data():
    sessions = [s for s in Session.objects.all() if 'trust' in s.config['app_sequence'] and s.config.get('city_code')]
    trust = TrustDataGetter(TPlayer, sessions)
    decision = DecisionGetter(Decision, sessions)
    question = QGetter(QPlayer, sessions)
    timer = TimeGetter(PageCompletion, sessions)
    getters = [trust, decision, question, timer]
    to_merge = []
    for i in getters:
        if i.data_exists():
            to_merge.append(i.get_data())
    if len(to_merge) > 0:
        merged = pd.concat(to_merge, sort=False, join='outer', axis=1)
        merged = reshuffle_data(merged)
        merged.reset_index(inplace=True)
        return merged
