import pandas as pd
from trust.models import Decision
from questionnaire.models import Player as QPlayer
from trust.models import Player as TPlayer
from django.db.models import Value, IntegerField, F, DecimalField
from django.db.models.functions import Cast
from otree.models_concrete import PageCompletion


def renamer(fields):
    def inner(f):
        if f in fields:
            return f'trustgame_{f}'
        return f

    return inner


def get_full_data():
    # get extra info from trust game
    def get_trust_data_df(Player):
        toconv = ['_payoff',
                  'endowment',
                  'stage1payoff',
                  'stage2payoff',
                  ]
        curconverter = {}
        for p in toconv:
            curconverter[f'trustgame_{p}'] = Cast(p, output_field=IntegerField())
        data = Player.objects.all().annotate(**curconverter).values()

        df = pd.DataFrame(list(
            data.values('session__code', 'participant__code', 'participant__time_started', 'city', 'partner_city',
                        '_role', 'city_order', 'participant__id_in_session', 'participant__label',
                        *curconverter.keys(), )))
        df.set_index('participant__code', inplace=True)
        df['participant__time_started'] = pd.to_datetime(df['participant__time_started'], unit='s').dt.strftime(
            '%B %d, %Y, %r')
        return df

    # get pivot table from decisions
    def get_decisions_wide_df(Decision):
        d = Decision.objects.all()
        df = pd.DataFrame(list(d.values('city__code', 'decision_type', 'owner__participant__code', 'answer')))
        df.rename(dict(owner__participant__code='participant__code'), axis='columns', inplace=True)

        table = pd.pivot_table(df, values='answer', index=['participant__code'],
                               columns=['decision_type', 'city__code'])
        table.columns = ['_'.join(col).strip() for col in table.columns.values]

        return table

    # get questionnaire
    def get_q_data(Player):
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
        data = Player.objects.all()
        fields = [q.name for q in Player._meta.get_fields() if q.name not in skip_fields]
        df = pd.DataFrame(list(data.values(*fields, 'participant__code', )))
        df.set_index('participant__code', inplace=True)
        return df

    # get time completion as pivot
    def get_time():
        pages = ['CQ1', 'CQ2', 'SenderDecisionP', 'SenderBeliefP', 'ReturnDecisionP', 'ReturnerBeliefP', 'Average2',
                 'Average3',
                 'Motivation', ]
        q = PageCompletion.objects.filter(page_name__in=pages)
        ps = q.values('participant__code', 'page_name', 'seconds_on_page')

        df = pd.DataFrame(list(ps))
        df['page_name'] = df['page_name'].apply(lambda x: f'time_{x}')
        table = pd.pivot_table(df, values='seconds_on_page', index=['participant__code'],
                               columns=['page_name'])

        return table

    trust_data = get_trust_data_df(TPlayer)
    decisions = get_decisions_wide_df(Decision)
    q = get_q_data(QPlayer)
    completion_time = get_time()
    merged = pd.concat([
        trust_data,
        q,
        decisions,
        completion_time

    ], sort=False, join='inner', axis=1)
    merged.reset_index(inplace=True)

    return merged
