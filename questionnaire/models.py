from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from .widgets import OtherRadioSelect
from django.utils.translation import gettext_lazy as _


def __(l):
    for i,j in l:
        print(_(j))
    return [(i, _(j)) for i, j in l]

a = [_('ф'),'ы']
b = [_(i) for i in a]
author = 'Philipp Chapkovski, HSE-Moscow'

doc = """
Post-experimental questionnaire for interregional project. 
"""


class Constants(BaseConstants):
    name_in_url = 'Questionnaire'
    players_per_group = None
    num_rounds = 1
    GENDER_CHOICES = [[0, 'Мужской'], [1, 'Женский']]
    MARITAL_STATUS_CHOICES =__([
        [1, 'Не женаты/не замужем'],
        [2, 'Женаты/замужем'],
        [3, 'В отношениях, но официально не состоите в браке'],
        [4, 'Разведены'],
        [5, 'Живете отдельно от супруга/и'],
        [6, 'Вдовец/Вдова'],
        [7, 'Затрудняюсь ответить']
    ])

    LIVING_CHOICES = [
        [1, 'С родителями'],
        [2, 'В общежитии'],
        [3, 'В съемной квартире'],
        [4, 'В отдельной квартитре'],
        [5, 'Другое']
    ]
    IncrementChoices5DNK = [
        [1, 'Безусловно увеличился'],
        [2, 'Скорее увеличился'],
        [3, 'Не изменился'],
        [4, 'Скорее уменьшился'],
        [5, 'Безусловно уменьшился'],
        [6, 'Затрудняюсь ответить'],
    ]
    RELIGION_CHOICES = [
        [1, 'Не исповедую никакой религии (атеист)'],
        [2, 'Католицизм'],
        [3, 'Протестантизм'],
        [4, 'Православие'],
        [5, 'Иудаизм'],
        [6, 'Ислам'],
        [7, 'Индуизм'],
        [8, 'Буддизм'],
        [9, 'Другую религию']
    ]
    SAME_MORAL_CHOICES = [
        [1, 'Совершенно согласен'],
        [2, 'Скорее согласен'],
        [3, 'И да и нет'],
        [4, 'Скорее не согласен'],
        [5, 'Совершенно не согласен'],
        [6, 'Затрудняюсь ответить'],
        [7, 'Без ответа, я атеист']
    ]
    CHURCH_ATTENDANCE_CHOICES = [
        [0, 'Вообще не бываю'],
        [1, '1 раз в месяц или реже'],
        [2, '2-3 раза в месяц'],
        [3, '4 раза в месяц или чаще'],
        [4, 'Затрудняюсь ответить'],
        [5, 'Без ответа, я атеист']
    ]
    JUSTIFIED_CHOICES = range(0, 11)
    RISK_CHOICES = range(0, 11)
    AGREEEMENT_CHOICES = [
        [1, 'Безусловно согласия, сплоченности'],
        [2, 'Скорее согласия, сплоченности'],
        [3, 'Скорее несогласия, разобщенности'],
        [4, 'Безусловно несогласия, разобщенности'],
        [5, 'Затрудняюсь ответить']
    ]
    SIMILAR_TRUST_CHOICES = [
        [1, 'Безусловно больше'],
        [2, 'Скорее больше'],
        [3, 'Одинаково'],
        [4, 'Скорее меньше'],
        [5, 'Безусловно меньше'],
        [6, 'Затрудняюсь ответить']
    ]
    SELF_TRUST_CHOICES = [
        [1, 'Вы доверчивы'],
        [2, 'Вы скорее доверчивы чем нет'],
        [3, 'Вы бываете и доверчивы и недоверчивы'],
        [4, 'Вы скорее недоверчивы'],
        [5, 'Вы недоверчивы'],
        [6, 'Затрудняюсь ответить']
    ]
    READY_HELP_CHOICES = [
        [1, 'Да'],
        [2, 'Скорее да чем нет'],
        [3, 'Скорее нет чем да'],
        [4, 'Нет'],
        [5, 'Затрудняюсь ответить']
    ]
    FEATURE_CHOICES = range(0, 11)
    SEPARATION_POWER_CHOICES = [
        [1, 'Разделение властей существует, система сдержек и противовесов реально работает'],
        [2, 'Разделение властей существует, несмотря на отдельные попытки нарушить систему сдержек и противовесов'],
        [3, 'Разделение властей существует формально, на практике система сдержек и противовесов работает плохо'],
        [4, 'Разделения властей нет, система сдержек и противовесов не работает'],
        [5, 'Затрудняюсь ответить'],
        [6, 'Отказ от ответа']
    ]
    INDEPENDENT_JUD_CHOICES = [
        [1, 'Суды независимы от других общественных институтов и некоррумпированы'],
        [2,
         'Суды в основном независимы, хотя иногда подвержены воздействию других общественных институтов и бывают случаи коррупции'],
        [3,
         'Независимость судов в значительной степени подорвана: они находятся во влиянием других общественных институтов и коррупции'],
        [4, 'Независимых судов в нашей стране нет'],
        [5, 'Затрудняюсь ответить'],
        [6, 'Отказ от ответа']
    ]
    CORRUPTION_CHOICES = [
        [1, 'Коррупция строго преследуется в соответствии с законом и подвергается публичному осуждению'],
        [2,
         'Коррупция в целом преследуется по закону и осуждается, однако иногда вовлеченным в нее людям удается найти лазейки и уйти от ответственности'],
        [3, 'Коррупция недостаточно преследуется по закону, и иногда подвергается публичному осуждению'],
        [4, 'Коррупция практически безнаказанна, и не осуждается публично'],
        [5, 'Затрудняюсь ответить'],
        [6, 'Отказ от ответа']
    ]
    CIVIL_RIGHTS_CHOICES = [
        [1, 'Гражданские права эффективно защищены законом, а их нарушение карается'],
        [2,
         'Гражданские права охраняются законом, но защита недостаточна, и нарушение этих прав не всегда преследуется'],
        [3,
         'Гражданские права обозначены в законе, но на практике нарушаются, и механизмы их защиты, как правило, неэффективны'],
        [4, 'Гражданские права систематически нарушаются, и механизмы их защиты отсутствуют'],
        [5, 'Затрудняюсь ответить'],
        [6, 'Отказ от ответа']
    ]
    SATIS_CHOICES = range(0, 11)
    HAPPY_CHOICES = [
        [0, 'Несчастливый человек'],
        [1, 'Счастливый человек'],
    ]
    RELATIVE_HAPPY_CHOICES = [
        [0, 'Менее счастливы чем они'],
        [1, 'В среднем так же счастлив, как и они'],
        [2, 'Более счастлив чем они']
    ]
    INCOME_CHOICES = [
        [1, 'Не хватает денег даже на еду'],
        [2, 'Хватает на еду, но не хватает на покупку одежды и обуви'],
        [3, 'Хватает на одежду и обувь, но не хватает на покупку мелкой бытовой техники'],
        [4,
         'Хватает денег на небольшие покупки, но покупка дорогих вещей (компьютера, стиральной машины, холодильника) требует накоплений или кредита'],
        [5,
         'Хватает денег на покупки для дома, но на покупку машины, дачи, квартиры необходимо копить или брать кредит'],
        [6, 'Можем позволить себе любые покупки без ограничений и кредитов']
    ]
    PARTY_CHOICES = [
        [1, 'Единая Россия'],
        [2, 'КПРФ'],
        [3, 'ЛДПР'],
        [4, 'Справедливая Россия'],
        [5, 'Яблоко'],
        [6, 'Другая партия'],
        [7, 'В России нет партии, которой  я симпатизирую'],
        [8, 'Я не интересуюсь политикой'],
        [9, 'Затрудняюсь ответить']
    ]
    AgreementChoices4DNK = [
        [1, 'Совершенно согласен'],
        [2, 'Скорее согласен'],
        [3, 'Скорее не согласен'],
        [4, 'Совершенно не согласен'],
        [5, 'Затрудняюсь ответить'],
    ]

    TrustChoices4DNK = [
        [1, 'Полностью доверяю'],
        [2, 'В некоторой степени доверяю'],
        [3, 'Не очень доверяю'],
        [4, 'Совсем не доверяю'],
        [5, 'Затрудняюсь ответить'],
    ]

    SimilarChoices6DNK = [
        [1, 'Очень похож на меня'],
        [2, 'Похож на меня'],
        [3, 'Отчасти похож на меня'],
        [4, 'Немного похож на меня'],
        [5, 'Не похож на меня'],
        [6, 'Совсем не похож на меня'],
        [7, 'Затрудняюсь ответить'],
    ]

    AgreementChoices5DNK = [
        [1, 'Совершенно согласен'],
        [2, 'Скорее согласен'],
        [3, 'И да и нет'],
        [4, 'Скорее не согласен'],
        [5, 'Совершенно не согласен'],
        [6, 'Затрудняюсь ответить'],
    ]

    Sibling4 = [
        [1, '0'],
        [2, '1'],
        [3, '2'],
        [4, '3'],
        [5, '4 или более'],
    ]

    Region6 = [
        [1, '0'],
        [2, '1'],
        [3, '2-3'],
        [4, '4-6'],
        [5, '7 или более'],
    ]
    # Survey1
    Inc5DNK = IncrementChoices5DNK
    # Survey2
    Agree4DNK = AgreementChoices4DNK
    # Survey3
    Trust4DNK = TrustChoices4DNK
    # Surveys4
    Similar6DNK = SimilarChoices6DNK
    # Survey5similar_newideas
    Agree5DNK = AgreementChoices4DNK
    # Survery6
    Sib4 = Sibling4
    # Survery7
    Reg6 = Region6
    SOURCE_CHOICES = [
        [0, 'Ничего не знаю о регионе'],
        [1, 'От родственников и друзей'],
        [2, 'Из социальных сетей (vk, instagram и др.'],
        [3, 'Из средств массовой информации (газеты, телевидение, интернет-медиа и др.)'],
        [4, 'В школе или университете'],
        [5, 'Другие источники'],
    ]
    BEEN_CHOICES = [
        [0, 'Да'],
        [1, 'Нет'],
    ]


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.payoff = 15
            p.participant.vars['questionnaire_payoff'] = p.payoff.to_real_world_currency(self.session)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def set_payoff(self):
        """Calculate payoff, which is zero for the survey"""
        self.payoff = 0

    # Motivation
    motivation_part1 = models.TextField(
        label='''Пожалуйста, вспомните ваши решения в части 1 эксперимента.
            Участник А: передать ли начальную сумму участнику В.
            Участник В: ничего не возвращать, вернуть все или вернуть лишь часть 30 токенов
            Чем Вы руководствовались, принимая эти решения?
            Почему Вы решили именно так?'''
    )

    motivation_part2 = models.TextField(
        label='''Пожалуйста, вспомните ваши решения в части 2 эксперимента.
            Участник А: оценить, какую часть 30 токенов участник В захочет вернуть.
            Участник В: оценить, хотел ли участник А передать Вам его начальную сумму.
            Чем Вы руководствовались, принимая эти решения?
            Почему Вы решили именно так?'''
    )

    field = models.PositiveIntegerField(label='Ваша специализация',
                                        choices=[[1, 'Экономика, финансы, менеджмент'],
                                                 [2, 'Социальные науки, психология, политология'], [3, 'Право'],
                                                 [4, 'Международные отношения'],
                                                 [5, 'Математика, информатика, анализ данных'],
                                                 [6, 'Естественные науки, инженерное дело'],
                                                 [7, 'Филология, гуманитарные науки'],
                                                 [8, 'Медиа, журналистика, дизайн'],
                                                 [9, 'Другое']],
                                        widget=OtherRadioSelect(other=(9, 'field_other')))

    field_other = models.CharField(
        label='''Если другое, то что именно?''',
        blank=True
    )

    degree = models.PositiveIntegerField(label='На какой программе Вы учитесь',
                                         choices=[
                                             [1, 'Бакалавриат'],
                                             [2, 'Специалитет'],
                                             [3, 'Магистратура'],
                                             [4, 'Аспирантура'],
                                             [5, 'Другое']
                                         ],
                                         widget=OtherRadioSelect(other=(5, 'degree_other')))

    degree_other = models.CharField(blank=True,
                                    label='''Если другое, то что именно?'''
                                    )

    studyear = models.PositiveIntegerField(
        label='''
           Год обучения (курс)''',
        min=0, max=8,
        initial=None)

    gender = models.BooleanField(initial=None,
                                 choices=Constants.GENDER_CHOICES,
                                 label='Ваш пол',
                                 widget=widgets.RadioSelect())

    age = models.PositiveIntegerField(label='Ваш возраст (полных лет)',
                                      min=13, max=95,
                                      initial=None)

    birthplace = models.CharField(
        label='''Место рождения (населенный пункт, регион)'''
    )

    GPA = models.CharField(
        label='''Ваш средний балл за все время учебы на программе (из 5)'''
    )

    marital_status = models.PositiveIntegerField(
        label='Ваш семейный статус',
        choices=Constants.MARITAL_STATUS_CHOICES,
        widget=widgets.RadioSelect()
    )

    language = models.BooleanField(
        label='На каком языке Вы обычно говорите дома?',
        choices=[
            [0, 'Русский'],
            [1, 'Другой (какой именно)']
        ],
        widget=OtherRadioSelect(other=(1, 'language_other'))
    )

    language_other = models.CharField(blank=True,
                                      label='''Если на другом языке, то на каком именно?'''
                                      )

    living = models.PositiveIntegerField(
        label='Вы живете...',
        choices=Constants.LIVING_CHOICES,
        widget=OtherRadioSelect(other=(5, 'living_other'))
    )

    living_other = models.CharField(blank=True,
                                    label='''Уточните где именно'''
                                    )

    city = models.PositiveIntegerField(
        label='''    Сколько человек (приблизительно) проживало в том населенном пункте, где Вы жили в возрасте 16 лет?''',
        min=1, max=30000000,
        initial=None)

    # Self-Determination

    nationality = models.CharField(
        label='''К какой национальности Вы себя относите?'''
    )

    religion = models.PositiveIntegerField(
        label='Какую религию Вы исповедуете?',
        choices=Constants.RELIGION_CHOICES,
        widget=OtherRadioSelect(other=(9, 'religion_other'))
    )

    religion_other = models.CharField(blank=True,
                                      label='''Уточните какую именно'''
                                      )

    religion_moral = models.PositiveIntegerField(
        label='''Насколько Вы согласны со следующим утверждением? "Люди, исповедующие другие религии, вероятно, 
        такие же глубоко моральные люди, как и те, что исповедуют Вашу религию."''',
        choices=Constants.SAME_MORAL_CHOICES,
        widget=widgets.RadioSelect()
    )

    religion_service = models.PositiveIntegerField(
        label='''Как часто Вы посещаете храм''',
        choices=Constants.CHURCH_ATTENDANCE_CHOICES,
        widget=widgets.RadioSelect()
    )

    community_local = models.PositiveIntegerField(
        label='''Я считаю себя членом местной общины (сообщества) жителей моего города''',
        choices=Constants.Agree4DNK
    )

    community_russian = models.PositiveIntegerField(
        label='''Я считаю себя россиянином''',
        choices=Constants.Agree4DNK
    )

    # Trust

    trust = models.PositiveIntegerField(
        label='''Как Вы считаете, в целом большинству людей можно доверять, или же при общении с другими людьми 
            осторожность никогда не повредит?''',
        choices=[
            [0, "Нужно быть очень осторожным с другими людьми"],
            [1, "Большинству людей можно вполне доверять"],
        ],
        widget=widgets.RadioSelect()
    )

    trust_family = models.IntegerField(
        label='''Ваша семья''',
        choices=Constants.Trust4DNK,
        widget=widgets.RadioSelectHorizontal
    )
    trust_neighbours = models.IntegerField(
        label='''Ваши соседи''',
        choices=Constants.Trust4DNK,
        widget=widgets.RadioSelectHorizontal
    )
    trust_acquant = models.IntegerField(
        label='''Люди, с которыми Вы лично знакомы''',
        choices=Constants.Trust4DNK,
        widget=widgets.RadioSelectHorizontal
    )
    trust_stranger = models.IntegerField(
        label='''Люди, с которыми Вы не знакомы''',
        choices=Constants.Trust4DNK,
        widget=widgets.RadioSelectHorizontal
    )
    trust_other_faith = models.IntegerField(
        label='''Люди другой веры''',
        choices=Constants.Trust4DNK,
        widget=widgets.RadioSelectHorizontal
    )
    trust_fiends = models.IntegerField(
        label='''Ваши друзья''',
        choices=Constants.Trust4DNK,
        widget=widgets.RadioSelectHorizontal
    )
    trust_politicians = models.IntegerField(
        label='''Политики''',
        choices=Constants.Trust4DNK,
        widget=widgets.RadioSelectHorizontal
    )

    trust_church = models.IntegerField(
        label='''
        Церковь''',
        choices=Constants.Trust4DNK
    )
    trust_army = models.IntegerField(
        label='''Армия''',
        choices=Constants.Trust4DNK
    )
    trust_press = models.IntegerField(
        label='''Пресса (печатные медиа)''',
        choices=Constants.Trust4DNK
    )
    trust_tv = models.IntegerField(
        label='''Телевидение''',
        choices=Constants.Trust4DNK
    )
    trust_tradeunion = models.IntegerField(
        label='''Профсоюзы''',
        choices=Constants.Trust4DNK
    )
    trust_police = models.IntegerField(
        label='''Полиция''',
        choices=Constants.Trust4DNK
    )
    trust_courts = models.IntegerField(
        label='''Суды''',
        choices=Constants.Trust4DNK
    )
    trust_government = models.IntegerField(
        label='''Правительство России''',
        choices=Constants.Trust4DNK
    )
    trust_parties = models.IntegerField(
        label='''Политические партии''',
        choices=Constants.Trust4DNK
    )
    trust_president = models.IntegerField(
        label='''Президент''',
        choices=Constants.Trust4DNK
    )
    trust_parliament = models.IntegerField(
        label='''Парламент России''',
        choices=Constants.Trust4DNK
    )
    trust_regional_authorities = models.IntegerField(
        label='''Региональная власть''',
        choices=Constants.Trust4DNK
    )
    trust_local_authorities = models.IntegerField(
        label='''Местная власть''',
        choices=Constants.Trust4DNK
    )
    trust_charity = models.IntegerField(
        label='''Гуманитарные и благотворительные организации''',
        choices=Constants.Trust4DNK
    )
    trust_CIS = models.IntegerField(
        label='''Содружество независимых государств (СНГ)''',
        choices=Constants.Trust4DNK
    )
    trust_UN = models.IntegerField(
        label='''Организация объединенных наций (ООН)''',
        choices=Constants.Trust4DNK
    )

    dtrust = models.IntegerField(
        label='По Вашему мнению, за последние годы изменился или не изменился уровень доверия людей друг к другу? Если изменился, то увеличился или уменьшился?',
        choices=Constants.Inc5DNK
    )

    # Values

    similar_newideas = models.IntegerField(
        label='''Для этого человека важно предлагать новые идеи, быть творческой личностью, идти своим путем''',
        choices=Constants.Similar6DNK
    )

    similar_wealthy = models.IntegerField(
        label='''Для этого человека важно быть богатым,  иметь много денег и дорогих вещей''',
        choices=Constants.Similar6DNK
    )

    similar_safety = models.IntegerField(
        label='''Для этого человека важно жить в безопасности, избегать всего, что может сулить опасность''',
        choices=Constants.Similar6DNK
    )

    similar_hedonic = models.IntegerField(
        label='''Для этого человека важно хорошо проводить время, баловать себя''',
        choices=Constants.Similar6DNK
    )

    similar_renowned = models.IntegerField(
        label='''Для этого человека важно быть очень успешным, чтобы окружающие знали о его достижениях''',
        choices=Constants.Similar6DNK
    )

    similar_adventurous = models.IntegerField(
        label='''Приключения и риск очень важны для этого человека, он стремится к жизни, полной захватывающих событий''',
        choices=Constants.Similar6DNK
    )

    similar_correct = models.IntegerField(
        label='''Для этого человека важно всегда вести себя правильно, не совершать поступков, которые люди не одобрили ''',
        choices=Constants.Similar6DNK
    )

    similar_care_environment = models.IntegerField(
        label='''Для этого человека важно заботиться об окружающей среде и природе''',
        choices=Constants.Similar6DNK
    )

    similar_tradition = models.IntegerField(
        label='''Для этого человека важно следовать традициям и обычаям, принятым в его семье или религии''',
        choices=Constants.Similar6DNK
    )

    justified_subsidies = models.IntegerField(
        label='''Получение государственных пособий, на которые у человека нет права''',
        choices=Constants.JUSTIFIED_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    justified_freeride = models.IntegerField(
        label='''Проезд без оплаты в общественном транспорте''',
        choices=Constants.JUSTIFIED_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    justified_theft = models.IntegerField(
        label='''Кража чужой собственности''',
        choices=Constants.JUSTIFIED_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    justified_tax_evasion = models.IntegerField(
        label='''Неуплата налогов, если есть такая возможность''',
        choices=Constants.JUSTIFIED_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    justified_corruption = models.IntegerField(
        label='''Получение взятки''',
        choices=Constants.JUSTIFIED_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    justified_violence = models.IntegerField(
        label='''Применение насилия в отношении других людей''',
        choices=Constants.JUSTIFIED_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    # Risk
    riskat = models.PositiveIntegerField(
        label='''Скажите, пожалуйста, насколько Вы в целом любите рисковать? ''',
        choices=Constants.RISK_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    riskfin = models.PositiveIntegerField(
        label='''В финансовых вопросах''',
        choices=Constants.RISK_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    risksport = models.PositiveIntegerField(
        label='''В свободное время и во время занятий спортом''',
        choices=Constants.RISK_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    riskprof = models.PositiveIntegerField(
        label='''В вашей профессии''',
        choices=Constants.RISK_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    riskhealth = models.PositiveIntegerField(
        label='''В том что касается вашего здоровья''',
        choices=Constants.RISK_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    riskstran = models.PositiveIntegerField(
        label='''В отношениях с незнакомыми людьми''',
        choices=Constants.RISK_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    # StatedPreferences
    moreagreement = models.PositiveIntegerField(
        label='''Как Вы думаете, сегодня в нашей стране среди людей больше согласия, сплоченности или несогласия, разобщенности?''',
        choices=Constants.AGREEEMENT_CHOICES,
        widget=widgets.RadioSelect()
    )

    similar_trust = models.PositiveIntegerField(
        label='''Людям, с которыми у Вас много общего, Вы доверяете больше, чем всем остальным, меньше чем остальным или же одинаково?''',
        choices=Constants.SIMILAR_TRUST_CHOICES,
        widget=widgets.RadioSelect()
    )

    trustful = models.PositiveIntegerField(
        label='''Можете ли Вы сказать о себе, что Вы доверчивый человек?''',
        choices=Constants.SELF_TRUST_CHOICES,
        widget=widgets.RadioSelect()
    )

    ready_help = models.PositiveIntegerField(
        label='''Готовы ли Вы тратить свои ресурсы на благое дело, даже если не рассчитываете ничего получить взамен?''',
        choices=Constants.READY_HELP_CHOICES,
        widget=widgets.RadioSelect()
    )

    dreadyhelp = models.IntegerField(
        label='По Вашему мнению, за последние годы изменился или не изменился уровень готовности людей помогать друг другу? Если изменился, то увеличился или уменьшился?',
        choices=Constants.Inc5DNK
    )

    freedom = models.PositiveIntegerField(
        label='''Некоторые люди чувствуют, что они обладают полной свободой выбора и контролируют свою жизнь, в
         то время как другие люди чувствуют, что то, что они делают, не имеет реального влияния на происходящее с ними. До какой степени эти
         характеристики применимы к Вам и Вашей жизни? Для ответа выберите значение на шкале от 0 до 10, где 0 означает "у меня нет свободы выбора", а 10
         означает "у меня полная свобода выбора":.
         ''',
        choices=Constants.FEATURE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    positive_reciprocity = models.PositiveIntegerField(
        label='''"Когда кто-либо мне помогает я стараюсь ответить тем же." Справедливо ли это суждение в отношении Вас? Для ответа выберите значение на шкале от 0 до 10,
         где 0 означает, что Вы «совершенно не готовы так поступать», а 10 означает, что Вы «готовы поступать именно так»:''',
        choices=Constants.FEATURE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    negative_reciprocity = models.PositiveIntegerField(
        label='''"Если со мной поступили несправедливо, я отомщу при первом же удобном случае, даже если это дорого мне обойдется."  Справедливо ли это суждение в отношении Вас? Для ответа выберите значение на шкале от 0 до 10,
         где 0 означает, что Вы «совершенно не готовы так поступать», а 10 означает, что Вы «готовы поступать именно так»''',
        choices=Constants.FEATURE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    abuse_you = models.PositiveIntegerField(
        label='''Как Вы думаете, если представится возможность, большинство людей попытались бы использовать вас в своих интересах, или вели бы себя порядочно?
         Для ответа выберите значение на шкале от 0 до 10, где 0 означает, что «люди обязательно попытаются вас использовать», а 10 означает, что «люди поведут себя порядочно»''',
        choices=Constants.FEATURE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    competition = models.PositiveIntegerField(
        label='''Как Вы думаете, конкуренция - это зло или благо?
             Для ответа выберите значение на шкале от 0 до 10, где 0 означает, что «конкуренция вредна, поскольку она побуждает у людей худшие качества», 
             а 10 означает, что «конкуренция - это благо, поскольку она побуждает людей лучше трудиться»''',
        choices=Constants.FEATURE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    fairness_general = models.PositiveIntegerField(
        label='''Как Вы думаете, могут ли люди в современном обществе разбогатеть только за счет других людей, или уровень благосостояния может вырасти у всех?
         Для ответа выберите значение на шкале от 0 до 10, где 0 означает, что «люди могут разбогатеть только за счет других», а 10 означает, что «благосостояние может вырасти у всех»''',
        choices=Constants.FEATURE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )
    fairness_russian = models.PositiveIntegerField(
        label='''Социальные различия между людьми в нашей стране в целом оправданны и справедливы''',
        choices=Constants.Agree5DNK
    )
    separation_power = models.PositiveIntegerField(
        label='''Как Вы считаете, в нашей стране сейчас имеет место разделение властей (законодательной, исполнительной и судебной) или же нет?''',
        choices=Constants.SEPARATION_POWER_CHOICES,
        widget=widgets.RadioSelect()
    )

    independent_judiciary = models.PositiveIntegerField(
        label='''Как Вы считаете, независимы ли в нашей стране суды?''',
        choices=Constants.INDEPENDENT_JUD_CHOICES,
        widget=widgets.RadioSelect()
    )

    corruption = models.PositiveIntegerField(
        label='''Что Вы думаете про борьбу с коррупцией в нашей стране?''',
        choices=Constants.CORRUPTION_CHOICES,
        widget=widgets.RadioSelect()
    )

    civil_rights = models.PositiveIntegerField(
        label='''До какой степени у нас в стране защищены гражданские права?''',
        choices=Constants.CIVIL_RIGHTS_CHOICES,
        widget=widgets.RadioSelect()
    )

    Ark_been = models.BooleanField(
        label='''Архангельск и Архангельская область''',
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Vlk_been = models.BooleanField(
        label='''Владивосток и Приморский край''',
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Vor_been = models.BooleanField(
        label='''Воронеж и Воронежская область''',
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Ekb_been = models.BooleanField(
        label='''Екатеринбург и Свердловская область''',
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Kaz_been = models.BooleanField(
        label='''Казань и республика Татарстан''',
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Mak_been = models.BooleanField(
        label='''Махачкала и республика Дагестан''',
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Mos_been = models.BooleanField(
        label='''Москва''',
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Nsk_been = models.BooleanField(
        label='''Новосибирск и Новосибирская область''',
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Per_been = models.BooleanField(
        label='''Пермь и Пермский край''',
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Ros_been = models.BooleanField(
        label='''Ростов-на-Дону и Ростовская область''',
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    SPb_been = models.BooleanField(
        label='''Санкт-Петербург''',
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Khb_been = models.BooleanField(
        label='''Харабовск и Хабаровский край''',
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    abroad_been = models.BooleanField(
        label='''Бывали ли Вы когда-либо за границей?''',
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Ark_source = models.PositiveIntegerField(
        label='''Архангельск и Архангельская область''',
        choices=Constants.SOURCE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Vlk_source = models.PositiveIntegerField(
        label='''Владивосток и Приморский край''',
        choices=Constants.SOURCE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Vor_source = models.PositiveIntegerField(
        label='''Воронеж и Воронежская область''',
        choices=Constants.SOURCE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Ekb_source = models.PositiveIntegerField(
        label='''Екатеринбург и Свердловская область''',
        choices=Constants.SOURCE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Kaz_source = models.PositiveIntegerField(
        label='''Казань и республика Татарстан''',
        choices=Constants.SOURCE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Mak_source = models.PositiveIntegerField(
        label='''Махачкала и республика Дагестан''',
        choices=Constants.SOURCE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Mos_source = models.PositiveIntegerField(
        label='''Москва''',
        choices=Constants.SOURCE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Nsk_source = models.PositiveIntegerField(
        label='''Новосибирск и Новосибирская область''',
        choices=Constants.SOURCE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Per_source = models.PositiveIntegerField(
        label='''Пермь и Пермский край''',
        choices=Constants.SOURCE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Ros_source = models.PositiveIntegerField(
        label='''Ростов-на-Дону и Ростовская область''',
        choices=Constants.SOURCE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    SPb_source = models.PositiveIntegerField(
        label='''Санкт-Петербург''',
        choices=Constants.SOURCE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Khb_source = models.PositiveIntegerField(
        label='''Харабовск и Хабаровский край''',
        choices=Constants.SOURCE_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Ark_rank = models.CharField(
        label='''Архангельск и Архангельская область'''
    )

    Vlk_rank = models.CharField(
        label='''Владивосток и Приморский край'''
    )

    Vor_rank = models.CharField(
        label='''Воронеж и Воронежская область'''
    )

    Ekb_rank = models.CharField(
        label='''Екатеринбург и Свердловская область'''
    )

    Kaz_rank = models.CharField(
        label='''Казань и республика Татарстан'''
    )

    Mak_rank = models.CharField(
        label='''Махачкала и республика Дагестан'''
    )

    Mos_rank = models.CharField(
        label='''Москва'''
    )

    Nsk_rank = models.CharField(
        label='''Новосибирск и Новосибирская область''')

    Per_rank = models.CharField(
        label='''Пермь и Пермский край'''
    )

    Ros_rank = models.CharField(
        label='''Ростов-на-Дону и Ростовская область'''
    )

    SPb_rank = models.CharField(
        label='''Санкт-Петербург'''
    )

    Khb_rank = models.CharField(
        label='''Харабовск и Хабаровский край'''
    )

    regional_income = models.CharField(
        label='''Как Вы считаете, каков среднемесячный доход жителей Вашего региона? Напишите пожалуйста Вашу оценку (в рублях в месяц)'''
    )

    regional_differences = models.PositiveIntegerField(
        label='''Согласны ли Вы с утверждением, что различия в уровне доходов между регионами России неоправданно велики''',
        choices=Constants.Agree5DNK
    )

    satis = models.PositiveIntegerField(
        label='''Учитывая все обстоятельства, насколько Вы удовлетворены вашей жизнью в целом в эти дни?  Для ответа выберите значение на шкале от 0 до 10,
         где 0 означает «совершенно не удовлетворен», а 10 - «полностью удовлетворен»)''',
        choices=Constants.SATIS_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    happy = models.BooleanField(
        label='''В целом я могу сказать, что я''',
        choices=Constants.HAPPY_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    happy_relative = models.PositiveIntegerField(
        label='''По сравнению с большинством окружающих вас людей, вы''',
        choices=Constants.RELATIVE_HAPPY_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    income = models.PositiveIntegerField(
        label='''Какое высказывание наиболее точно описывает финансовое положение вашей семьи?''',
        choices=Constants.INCOME_CHOICES,
        widget=widgets.RadioSelect()
    )

    elder_sibling = models.PositiveIntegerField(
        label='''Сколько у вас старших братьев или сестер?''',
        choices=Constants.Sib4
    )

    younger_sibling = models.PositiveIntegerField(
        label='''Сколько у вас младших братьев или сестер?''',
        choices=Constants.Sib4
    )

    father_born = models.CharField(blank=True,
                                   label='''В каком регионе родился Ваш отец (если не знаете оставьте поле пустым)?''',
                                   )

    mother_born = models.CharField(blank=True,
                                   label='''В каком регионе родилась Ваша мать (если не знаете оставьте поле пустым)?''',
                                   )

    regions_been = models.PositiveIntegerField(
        label='''В скольких регионах России (не считая вашего) вам случалось бывать)?''',
        choices=Constants.Reg6
    )

    honest_Russia = models.PositiveIntegerField(
        label='''В нынешней России честному человеку трудно достичь каких-то высот, занять высокое положение в обществе''',
        choices=Constants.Agree5DNK
    )

    party_Russia = models.PositiveIntegerField(
        label='''Сторонником какой политической партии вы являетесь, или по крайней мере,симпатизируете ей? ''',
        choices=Constants.PARTY_CHOICES,
        widget=OtherRadioSelect(other=(6, 'party_other'))
    )

    party_other = models.CharField(blank=True,
                                   label='''Если Вы сторонник другой партии, укажите какой именно''',
                                   )

    other_city = models.CharField(
        label='''Как Вы думаете, со студентами из какого города вы взаимодействовали в ходе этой экспериментальной сессии?'''
    )

    def get_rank_fields(self):
        # not the best decision if someone adds other fields ending with _rank... thoough
        r = [dict(name=f.name, label=f.verbose_name) for f in self._meta.get_fields() if
             f.name.endswith('_rank')]
        return r
