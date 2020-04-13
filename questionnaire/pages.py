from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


# from otreeutils.surveys import SurveyPage
#
# class SurveyPage1(SurveyPage):
#     pass
#
# from otreeutils.surveys import setup_survey_pages
#
# survey_pages = [
#     SurveyPage1
# ]
#
# setup_survey_pages(Player, survey_pages)   # Player from "models"

class Motivation(Page):
    form_model = 'player'
    form_fields = ['motivation_part1',
                   'motivation_part2',
                   ]


class Personal1(Page):
    form_model = 'player'
    form_fields = ['age',
                   'gender',
                   'field',
                   'field_other',
                   'degree',
                   'degree_other',
                   'studyear',
                   'gender',
                   'age',
                   'birthplace',
                   'GPA',
                   'marital_status',
                   'language',
                   'language_other',
                   'living',
                   'living_other',
                   'city'
                   ]


class SelfDetermination(Page):
    form_model = 'player'
    form_fields = [
        'nationality',
        'religion',
        'religion_other',
        'religion_moral',
        'religion_service',
        'community_local',
        'community_russian'
    ]


from .forms import TrustForm
from django.forms.models import modelform_factory


class Trust(Page):
    joined_fields = [{"title": 'Скажите пожалуйста, насколько Вы доверяете следующим категориям людей:',
                      "fields": ['trust_family',
                                 'trust_neighbours',
                                 'trust_acquant',
                                 'trust_stranger',
                                 'trust_other_faith',
                                 'trust_fiends',
                                 'trust_politicians', ]}]

    def get_form_class(self):
        form_model = self._get_form_model()
        fields = self.get_form_fields()
        return modelform_factory(form_model, fields=fields, form=TrustForm)

    def get_form(self, data=None, files=None, **kwargs):
        cls = self.get_form_class()
        return cls(self.joined_fields, data=data, files=files, view=self, **kwargs)

    form_model = 'player'
    form_fields = [
        'trust',
        #    'catrust',
        'trust_family',
        'trust_neighbours',
        'trust_acquant',
        'trust_stranger',
        'trust_other_faith',
        'trust_fiends',
        'trust_politicians',
        #     'catrust_institutions',
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
    form_model = 'player'
    form_fields = [
        'similar_newideas',
        'similar_wealthy',
        'similar_safety',
        'similar_hedonic',
        'similar_renowned',
        'similar_adventurous',
        'similar_correct',
        'similar_care_environment',
        'similar_tradition',
        'justified_subsidies',
        'justified_freeride',
        'justified_theft',
        'justified_tax_evasion',
        'justified_corruption',
        'justified_violence'
    ]


class Risk(Page):
    form_model = 'player'
    form_fields = [
        'riskat',
        #    'catrisk',
        'riskfin',
        'risksport',
        'riskprof',
        'riskhealth',
        'riskstran'
    ]


class StatedPreferences(Page):
    form_model = 'player'
    form_fields = [
        'moreagreement',
        'similar_trust',
        'trustful',
        'ready_help',
        'dreadyhelp',
        'freedom',
        'positive_reciprocity',
        'negative_reciprocity',
        'abuse_you',
        'competition',
        'fairness_general',
        'fairness_russian',
        'separation_power',
        'independent_judiciary',
        'corruption',
        'civil_rights'
    ]


class Region(Page):
    form_model = 'player'
    form_fields = [
        'Ark_been',
        'Vlk_been',
        'Vor_been',
        'Ekb_been',
        'Kaz_been',
        'Mak_been',
        'Mos_been',
        'Nsk_been',
        'Per_been',
        'Ros_been',
        'SPb_been',
        'Khb_been',
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
        'regional_income',
        'regional_differences'
    ]


class Personal2(Page):
    form_model = 'player'
    form_fields = [
        'satis',
        'happy',
        'happy_relative',
        'income',
        'elder_sibling',
        'younger_sibling',
        'father_born',
        'mother_born',
        'regions_been',
        'honest_Russia',
        'party_Russia',
        'party_other',
        'other_city'
    ]


page_sequence = [
    # Motivation,
    # Personal1,
    # SelfDetermination,
    Trust,
    # Values,
    # Risk,
    # StatedPreferences,
    # Region,
    # Personal2
]
