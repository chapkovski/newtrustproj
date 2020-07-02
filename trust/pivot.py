import pandas as pd
from trust.models import Decision
from questionnaire.models import Player as QPlayer
from trust.models import Player as TPlayer
from django.db.models import Value, IntegerField, F, DecimalField
from django.db.models.functions import Cast
from otree.models_concrete import PageCompletion
from otree.models import Session

def renamer(oldname):
    newname = oldname.strip('_').replace('__', '_')
    return newname


def reshuffle_data(data):
    data.rename(renamer, axis='columns', inplace=True)
    data = data * 1
    data['role'] = data['role'].replace({'receiver': 1, 'sender': 0, }).fillna('')
    return data


def get_full_data():
    # get extra info from trust game
    def get_trust_data_df(Player, sessions):
        toconv = ['_payoff',
                  'endowment',
                  'stage1payoff',
                  'stage2payoff',
                  ]
        curconverter = {}
        for p in toconv:
            curconverter[f'trustgame_{p}'] = Cast(p, output_field=IntegerField())
        data = Player.objects.filter(session__in=sessions).annotate(**curconverter).values()

        df = pd.DataFrame(list(
            data.values('session__code', 'participant__code', 'participant__time_started', 'city',
                        '_role', 'city_order', 'participant__id_in_session', 'participant__label',
                        'cq1_counter', 'cq2_counter',
                        *curconverter.keys(), )))
        df.set_index('participant__code', inplace=True)
        df['participant__time_started'] = pd.to_datetime(df['participant__time_started'], unit='s').dt.strftime(
            '%B %d, %Y, %r')
        return df

    # get pivot table from decisions
    def get_decisions_wide_df(Decision,sessions):
        d = Decision.objects.filter(owner__session__in=sessions,
                                    answer__isnull=False)
        if d.count()>0:
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


    sessions =[s for s in  Session.objects.all() if 'trust' in s.config['app_sequence'] and s.config.get('city_code')]
    trust_data = get_trust_data_df(TPlayer, sessions)
    to_merge = [trust_data]
    decisions = get_decisions_wide_df(Decision, sessions)
    if decisions:
        to_merge.append(decisions)
    # Obviously for testing we don't have a questionnaire.
    if QPlayer.objects.all().count() > 0:
        q = get_q_data(QPlayer)
        completion_time = get_time()
        to_merge.extend([q, completion_time])
    merged = pd.concat(to_merge, sort=False, join='inner', axis=1)
    merged = reshuffle_data(merged)
    merged.reset_index(inplace=True)

    return merged
