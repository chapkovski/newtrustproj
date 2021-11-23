from django.utils.translation import gettext_lazy as _
from .generic_pages import Page
from django.conf import settings
import json


class IntroQ(Page):
    pass


class Motivation(Page):
    form_model = 'player'
    form_fields = ['motivation_part1',
                   'motivation_part2',
                   'who_was_other_city',
                   'who_was_other_city_other'
                   ]


class Personal1(Page):
    special_fields = ['occupation_parent',
                      'occupation_child',
                      ]
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'education',
        'is_occupied',
        'self_employed',
        'occupation_status',
        'occupation_status_other',
        'occupation_parent',
        'occupation_child',

    ]


class SelfDetermination(Page):
    form_model = 'player'
    form_fields = [

        'religion',
        'religion_other',
        'religion_moral',
        'religion_service',
        'community_local',
        'community_russian'
    ]
    joined_fields = [{"title": _(
        'Насколько вы согласны или не согласны с каждым из следующих утверждений о том, как вы видите себя?'),
        "fields": [
            'community_local',
            'community_russian'
        ]}, ]


class Trust(Page):
    joined_fields = [{"title": _('Укажите, пожалуйста, насколько Вы доверяете следующим категориям людей:'),
                      "fields": ['trust_family',
                                 'trust_neighbours',
                                 'trust_acquant',
                                 'trust_stranger',
                                 'trust_other_faith',
                                 'trust_fiends',
                                 'trust_politicians', ]},
                     {"title": _('Укажите, пожалуйста, насколько Вы доверяете следующим организациям и институтам:'),
                      "fields": [
                          'trust_church',
                          'trust_army',
                          'trust_press',
                          'trust_tv',
                          'trust_tradeunion',
                          'trust_police',
                          'trust_courts',
                          'trust_government',
                          'trust_parties',
                          'trust_president',
                          'trust_parliament',
                          'trust_regional_authorities',
                          'trust_local_authorities',
                          # 'trust_charity',
                          # 'trust_CIS',
                          # 'trust_UN',
                      ]}
                     ]

    form_model = 'player'
    form_fields = [
        'general_trust',
        'trust_family',
        'trust_neighbours',
        'trust_acquant',
        'trust_stranger',
        'trust_other_faith',
        'trust_fiends',
        'trust_politicians',
        'trust_church',
        'trust_army',
        'trust_press',
        'trust_tv',
        'trust_tradeunion',
        'trust_police',
        'trust_courts',
        'trust_government',
        'trust_parties',
        'trust_president',
        'trust_parliament',
        'trust_regional_authorities',
        'trust_local_authorities',
        # 'trust_charity',
        # 'trust_CIS',
        # 'trust_UN',
        # 'dtrust'
    ]


class Values(Page):
    joined_fields = [{
        "title": _(
            'Вам кажется, что вы...:'),
        "fields": [
            'big5_1',
            'big5_2',
            'big5_3',
            'big5_4',
            'big5_5',
            'big5_6',
            'big5_7',
            'big5_8',
            'big5_9',
            'big5_10',
            'big5_11',
        ]},

        {"title": _("""Укажите, насколько то, о чем говорится ниже, заслуживает оправдания? Для ответа выберите значение на шкале от 1 до 10, 
        где 1 означает "никогда не заслуживает оправдания", а 10 означает "всегда заслуживает оправдания"."""),
         "fields": [
             'justified_subsidies',
             'justified_freeride',
             'justified_theft',
             'justified_tax_evasion',
             'justified_corruption',
             'justified_violence'
         ]},
    ]

    form_model = 'player'
    form_fields = [
        'big5_1',
        'big5_2',
        'big5_3',
        'big5_4',
        'big5_5',
        'big5_6',
        'big5_7',
        'big5_8',
        'big5_9',
        'big5_10',
        'big5_11',

        'justified_subsidies',
        'justified_freeride',
        'justified_theft',
        'justified_tax_evasion',
        'justified_corruption',
        'justified_violence'
    ]


class Risk(Page):
    form_model = 'player'
    joined_fields = [
        {"title": _("""Люди могут вести себя по-разному в разных ситуациях. Как бы Вы оценили своё желание брать на себя риски в следующих ситуациях? 
            Для ответа выберите значение на шкале от 0 до 10, где  0 означает, что Вы «совершенно не готовы рисковать», а 10 означает, что Вы «охотно идете на риск».
            """),
         "fields": [

             'risk_fin',
             'risk_sport',
             'risk_prof',
             'risk_health',
             'risk_strangers',
             'risk_drive'
         ]},
    ]
    form_fields = [
        'risk_general',
        'risk_fin',
        'risk_sport',
        'risk_prof',
        'risk_health',
        'risk_strangers',
        'risk_drive'
    ]


class StatedPreferences1(Page):
    template_name = 'questionnaire/StatedPreferences.html'
    form_model = 'player'
    form_fields = [
        'moreagreement',
        'similar_trust',
        'trustful',
        'ready_help',
        # 'dreadyhelp',

    ]


class StatedPreferences2_1(Page):
    template_name = 'questionnaire/StatedPreferences2.html'
    form_model = 'player'
    form_fields = [
        'freedom',
        'competition',
        'fairness_general',

    ]

    def vars_for_template(self) -> dict:
        return {'range110': range(1, 11),
                }


class StatedPreferences2_2(Page):
    template_name = 'questionnaire/StatedPreferences2.html'
    form_model = 'player'
    form_fields = [

        'positive_reciprocity',
        'negative_reciprocity',
        'abuse_you',

    ]

    def vars_for_template(self) -> dict:
        return {
            'range1010': range(0, 11)}


class StatedPreferences3(Page):
    template_name = 'questionnaire/StatedPreferences.html'
    form_model = 'player'
    form_fields = [
        'fairness_russian',
        'separation_power',
        'independent_judiciary',
        'corruption',
        'civil_rights'
    ]


class RegionsKnowledge(Page):
    form_model = 'player'
    blocked_fields = ['Ark_source',
                      'Vlk_source',
                      'Vor_source',
                      'Ekb_source',
                      'Kaz_source',
                      'Mak_source',
                      'Mos_source',
                      'Nsk_source',
                      'Per_source',
                      'Ros_source',
                      'SPb_source',
                      'Khb_source', ]

    form_fields = [
        'regions_been',
        'abroad_been',
        'Ark_source',
        'Vlk_source',
        'Vor_source',
        'Ekb_source',
        'Kaz_source',
        'Mak_source',
        'Mos_source',
        'Nsk_source',
        'Per_source',
        'Ros_source',
        'SPb_source',
        'Khb_source',
    ]


class RegionsIncome(Page):
    form_model = 'player'
    rankqs = [
        'Ark_rank',
        'Vlk_rank',
        'Vor_rank',
        'Ekb_rank',
        'Kaz_rank',
        'Mak_rank',
        'Mos_rank',
        'Nsk_rank',
        'Per_rank',
        'Ros_rank',
        'SPb_rank',
        'Khb_rank',
    ]

    form_fields = [

        'Ark_rank',
        'Vlk_rank',
        'Vor_rank',
        'Ekb_rank',
        'Kaz_rank',
        'Mak_rank',
        'Mos_rank',
        'Nsk_rank',
        'Per_rank',
        'Ros_rank',
        'SPb_rank',
        'Khb_rank',
        'rank_comment',
        'regional_differences',
        'regional_income',
        'relative_position_in_region',

    ]


class Personal2(Page):
    form_model = 'player'
    form_fields = [

        'satis',
        'happy',
        'happy_relative',
        'income',
        'honest_Russia',
        'party_Russia',
        'party_other',
        'birthplace',
        'marital_status',
        'language',
        'language_other',
        'ethnicity',
        'ethnicity_other',
        'living',
        'living_other',
        'city_size',
    ]

    def vars_for_template(self):
        return dict(GOOGLE_API_KEY=settings.GOOGLE_API_KEY)


class LastQ(Page):
    form_model = 'player'
    form_fields = ['comment']


# new pages

class SES(Page):
    form_fields = ["gender",
                   "smoke",
                   "income",
                   "fin_situation_change",
                   "best_intentions",
                   "fast_drive",
                   "general_trust",
                   "plans_to_move_WP85",
                   "where_to_move_WP3120",
                   ]


class NewPage(Page):
    def get_context_data(self, **context):
        r = super().get_context_data(**context)
        r['maxpages'] = self.participant._max_page_index
        r['page_index'] = self._index_in_pages
        r['progress'] = f'{int(self._index_in_pages / self.participant._max_page_index * 100):d}'
        return r

    def title(self):
        return self.__class__.__name__

    template_name = 'questionnaire/Q1.html'
    form_model = 'player'


class Income(NewPage):
    form_fields = [

        "reduce_income_diff",
        "regional_income_changed",
    ]


class IncomeScale(Page):
    template_name = 'questionnaire/IncomeScale.html'

    def post(self):
        data = json.loads(self.request.POST.get('surveyholder')).get('income_scale')
        self.player.income_scale = data
        return super().post()


class IncomeScaleFamily(Page):
    template_name = 'questionnaire/IncomeScaleFamily.html'

    def post(self):
        data = json.loads(self.request.POST.get('surveyholder')).get('income_scale_family')
        self.player.income_scale_family = data
        return super().post()


class IncomePyramid(Page):
    template_name = 'questionnaire/IncomePyramid.html'
    form_model = 'player'
    form_fields = ['income_pyramid']


class IncomePyramidRegional(Page):
    template_name = 'questionnaire/IncomePyramidRegional.html'
    form_model = 'player'
    form_fields = ['income_pyramid_regional']


class Lits2020(Page):
    template_name = 'questionnaire/Lits2020.html'
    form_model = 'player'
    form_fields = [
        'lits_equal',
        'lits_ownership',
        'lits_obey',
        'lits_authorities',
        'lits_wealthy',
        'lits_party'

    ]

    def vars_for_template(self):
        items = [
            dict(name='lits_equal',
                 left="Нужно уменьшить разницу доходов",
                 right="Нужно увеличить разницу доходов, чтобы люди прилагали больше усилий"),
            dict(name='lits_ownership',
                 left="Долю частной собственности в бизнесе и промышленности следует увеличить",
                 right="Нужно увеличить долю государственной собственности в бизнесе и промышленности"),
            dict(name='lits_obey', left="Люди должны подчиняться закону без исключения",
                 right="Бывают моменты, когда у людей есть веские причины нарушать закон", ),
            dict(name='lits_authorities',
                 left='Как граждане мы должны более активно подвергать сомнению действия наших властей',
                 right='Сегодня в нашей стране мы должны проявлять больше уважения к нашим властям'),
            dict(name='lits_wealthy',
                 left="То, что богатые люди влияют на то, как правительство управляет этой страной, не является проблемой",
                 right="Богатые люди часто используют свое влияние на правительство в своих собственных интересах, и для предотвращения этого необходимы более строгие правила"),
            dict(name='lits_party',
                 left="Финансовая поддержка политических партий и кандидатов, оказываемая частными компаниями, должна быть полностью запрещена",
                 right="Не должно быть никаких ограничений на финансовую поддержку политических партий или кандидатов, оказываемую частными компаниями")

        ]
        return dict(choices=range(1, 11), items=items)


class AltruismAndTrust(Page):
    template_name = 'questionnaire/AltruismAndTrust.html'

    def post(self):
        data = json.loads(self.request.POST.get('surveyholder'))
        altruism = data.get('altruism')
        if altruism:
            for k, v in altruism.items():
                setattr(self.player, k, v)
        return super().post()


class Patience(Page):
    def post(self):
        data = json.loads(self.request.POST.get('surveyholder')).get('patience')
        if data:
            for k, v in data.items():
                setattr(self.player, k, v.get('col1'))
        return super().post()

    template_name = 'questionnaire/Patience.html'


class Demographics(Page):
    form_model = 'player'
    form_fields = [
        "years_lived_current_city",
        "years_lived_birth_city",
        "lived_other_city",

    ]


class ChildrenQualities(Page):
    template_name = 'questionnaire/ChildrenQualities.html'

    def post(self):
        data = json.loads(self.request.POST.get('surveyholder')).get('children_qualities')
        if data:
            for i in data:
                if hasattr(self.player, i):
                    setattr(self.player, i, 1)
        return super().post()


class SES(NewPage):
    form_model = 'player'
    form_fields = [
        "smoke",
        "fin_situation_change",
        "best_intentions",
        "fast_drive",
        "plans_to_move_WP85",
        "where_to_move_WP3120",
    ]


# new pages  END

page_sequence = [
    IntroQ,
    Motivation,
    Personal1,
    RegionsKnowledge,
    RegionsIncome,
    Trust,
    StatedPreferences1,
    StatedPreferences2_1,
    StatedPreferences2_2,
    StatedPreferences3,
    SelfDetermination,
    Values,
    Risk,
    Personal2,
    LastQ,
    Income,
    IncomeScale,
    IncomeScaleFamily,
    IncomePyramid,
    IncomePyramidRegional,
    Lits2020,
    AltruismAndTrust,
    Patience,
    ChildrenQualities,
    SES,
]
