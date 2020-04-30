from django.utils.translation import gettext_lazy as _
from .generic_pages import Page
from django.conf import settings

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
                      'birthplace']
    form_model = 'player'
    form_fields = [
        'age',
                   'gender',
                   'education',
                   'occupation_status',
                   'occupation_status_other',
                   'occupation_parent',
                   'occupation_child',

                   ]
    def vars_for_template(self):
        return dict(GOOGLE_API_KEY=settings.GOOGLE_API_KEY)

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
    joined_fields = [{"title": _('Насколько вы согласны или не согласны с каждым из следующих утверждений о том, как вы видите себя?'),
                      "fields": [
                          'community_local',
                          'community_russian'
                      ]}, ]


class Trust(Page):
    joined_fields = [{"title": _('Скажите пожалуйста, насколько Вы доверяете следующим категориям людей:'),
                      "fields": ['trust_family',
                                 'trust_neighbours',
                                 'trust_acquant',
                                 'trust_stranger',
                                 'trust_other_faith',
                                 'trust_fiends',
                                 'trust_politicians', ]},
                     {"title": _('Скажите пожалуйста, насколько Вы доверяете следующим организациям и институтам:'),
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
                          'trust_charity',
                          'trust_CIS',
                          'trust_UN',
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
        'trust_charity',
        'trust_CIS',
        'trust_UN',
        'dtrust'
    ]


class Values(Page):
    joined_fields = [{
        "title": _(
            'Ниже представлены краткие описание некоторых людей. До какой степени каждый из описанных людей похож или не похож на вас?:'),
        "fields": [
            'similar_newideas',
            'similar_wealthy',
            'similar_safety',
            'similar_hedonic',
            'similar_renowned',
            'similar_care_nearby',
            'similar_adventurous',
            'similar_correct',
            'similar_care_environment',
            'similar_tradition',
            'similar_care_society',
        ]},

        {"title": _("""Скажите, насколько то, о чем говорится ниже, заслуживает оправдания? Для ответа выберите значение на шкале от 1 до 10, 
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
        'similar_newideas',
        'similar_wealthy',
        'similar_safety',
        'similar_hedonic',
        'similar_renowned',
        'similar_care_nearby',
        'similar_adventurous',
        'similar_correct',
        'similar_care_environment',
        'similar_tradition',
        'similar_care_society',

        'justified_subsidies',
        'justified_freeride',
        'justified_theft',
        'justified_tax_evasion',
        'justified_corruption',
        'justified_violence'
    ]


class Risk(Page):
    form_model = 'player'
    joined_fields = [{"title": _("""Люди могут вести себя по-разному в разных ситуациях. Как бы Вы оценили своё желание брать на себя риски в следующих ситуациях? 
        Для ответа выберите значение на шкале от 0 до 10, где  0 означает, что Вы «совершенно не готовы рисковать», а 10 означает, что Вы «охотно идете на риск».
        """),
                      "fields": [
                          'risk_general',
                          'risk_fin',
                          'risk_sport',
                          'risk_prof',
                          'risk_health',
                          'risk_strangers',
                          'risk_drive'
                      ]}, ]
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
        'dreadyhelp',

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
        'regional_differences',
        'regional_income',
        'relative_position_in_region',

    ]


class Personal2(Page):
    form_model = 'player'
    form_fields = [
        'birthplace',
        'marital_status',
        'language',
        'language_other',
        'ethnicity',
        'ethnicity_other',
        'living',
        'living_other',
        'city_size',
        'satis',
        'happy',
        'happy_relative',
        'income',
        'honest_Russia',
        'party_Russia',
        'party_other',

    ]


page_sequence = [
    # Motivation,
    # Personal1,
    # RegionsKnowledge,
    # RegionsIncome,
    # Trust,
    # StatedPreferences1,
    # StatedPreferences2_1,
    # StatedPreferences2_2,
    # StatedPreferences3,
    # SelfDetermination,
    Values,
    # Risk,
    # Personal2
]
