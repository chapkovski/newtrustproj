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
from .widgets import LikertWidget, BlockedCheckbox

from django.conf import settings

author = _('Philipp Chapkovski, HSE-Moscow')

doc = _("""
Post-experimental questionnaire for interregional project. 
""")


class Constants(BaseConstants):
    name_in_url = _('Questionnaire')
    players_per_group = None
    num_rounds = 1
    HARD_TO_SAY_CHOICE = [999, _('Затрудняюсь ответить')]
    CITIES = [(int(i.get('code')), i.get('name')) for i in settings.CITIES] + [(13, _('Другой'))]
    GENDER_CHOICES = [[0, _('Мужской')], [1, _('Женский')]]
    IS_OCCUPIED_CHOICES = [[False, _('Нет')], [True, _('Да')]]
    OCCUPATION_PARENT_CHOICES = [
        [1, _("Руководители")],
        (2, _("Специалисты высшего уровня квалификации")),
        (3, _("Специалисты среднего уровня квалификации")),
        (4, _("Служащие, занятые подготовкой и оформлением документации, учетом и обслуживанием")),
        (5, _("Работники сферы обслуживания и торговли, охраны граждан и собственности")),
        (6, _("Квалифицированные работники сельского и лесного хозяйства, рыбоводства и рыболовства")),
        (7, _("Квалифицированные рабочие промышленности, строительства, транспорта и рабочие родственных занятий")),
        (8, _("Операторы производственных установок и машин, сборщики и водители")),
        (9, _("Неквалифицированные рабочие")),
        (0, _("Военнослужащие")),
    ]
    OCCUPATION_CHILD_CHOICES = [
        (11, _("Руководители высшего звена, высшие должностные лица и законодатели")),
        (12, _("Управляющие в корпоративном секторе и в других организациях")),
        (13, _("Руководители подразделений в сфере производства и специализированных сервисных услуг")),
        (14, _(
            "Руководители в гостиничном и ресторанном бизнесе, розничной и оптовой торговле и родственных сферах обслуживания")),
        (21, _("Специалисты в области науки и техники")),
        (22, _("Специалисты в области здравоохранения")),
        (23, _("Специалисты в области образования")),
        (24, _("Специалисты в сфере бизнеса и администрирования")),
        (25, _("Специалисты по информационно-коммуникационным технологиям (ИКТ)")),
        (26, _("Специалисты в области права, гуманитарных областей и культуры")),
        (31, _("Специалисты-техники в области науки и техники")),
        (32, _("Средний медицинский персонал здравоохранения")),
        (33, _("Средний специальный персонал по экономической и административной деятельности")),
        (34, _(
            "Средний специальный персонал в области правовой, социальной работы, культуры, спорта и родственных занятий")),
        (35, _("Специалисты-техники в области информационно-коммуникационных технологий (ИКТ)")),
        (41, _("Служащие общего профиля и обслуживающие офисную технику")),
        (42, _("Служащие сферы обслуживания населения")),
        (43, _("Служащие в сфере обработки числовой информации и учета материальных ценностей")),
        (44, _("Другие офисные служащие")),
        (51, _("Работники сферы индивидуальных услуг")),
        (52, _("Продавцы")),
        (53, _("Работники, оказывающие услуги по индивидуальному уходу")),
        (54, _("Работники служб, осуществляющих охрану граждан и собственности")),
        (61, _("Квалифицированные работники сельского хозяйства, производящие товарную продукцию")),
        (62, _("Товарные производители лесной и рыбной продукции и охотники")),
        (63, _(
            "Квалифицированные работники сельского хозяйства, рыболовства, охотники и сборщики урожая, производящие продукцию для личного потребления")),
        (71, _("Рабочие, занятые в строительстве, и рабочие родственных занятий (за исключением электриков)")),
        (72, _("Рабочие, занятые в металлообрабатывающем и машиностроительном производстве, механики и ремонтники")),
        (73, _(
            "Рабочие, занятые изготовлением прецизионных инструментов и приборов, рабочие художественных промыслов и полиграфического производства")),
        (74, _("Рабочие в области электротехники и электроники")),
        (75,
         _(
             "Рабочие пищевой, деревообрабатывающей, текстильной и швейной промышленности и рабочие родственных занятий")),
        (81, _("Операторы промышленных установок и стационарного оборудования")),
        (82, _("Сборщики")),
        (83, _("Водители и операторы подвижного оборудования")),
        (91, _("Уборщики и прислуга")),
        (92, _("Неквалифицированные рабочие сельского и лесного хозяйства, рыбоводства и рыболовства")),
        (93, _(
            "Неквалифицированные рабочие, занятые в горнодобывающей промышленности, строительстве, обрабатывающей промышленности и на транспорте")),
        (94, _("Помощники в приготовлении пищи")),
        (95, _("Уличные торговцы и другие неквалифицированные работники, оказывающие различные уличные услуги")),
        (96, _("Неквалифицированные работники по сбору мусора и другие неквалифицированные работники"))
    ]
    RELATIVE_POSITION_CHOICES = [
        (1, _('...ниже, чем в среднем в вашем городе')),
        (2, _('...такой же, как в среднем в вашем городе')),
        (3, _('...выше, чем в среднем в вашем городе')),
        HARD_TO_SAY_CHOICE
    ]
    ETHNICITY_CHOICES = [
        (1, _('Русской')),
        (2, _('Другой')),
        HARD_TO_SAY_CHOICE
    ]

    EDUCATION_CHOICES = [
        [1, _('Средняя школа')],
        [2, _('Среднее профессиональное образование')],
        [3, _('Незаконченное высшее образование')],
        [4, _('Высшее образование')],
        [5, _('Два и более диплома / Ученая степень')],
    ]
    OCCUPATION_STATUS_CHOICES = [
        [1, _('Ученик средней школы, ПТУ')],
        [2, _('Студент дневного вуза, техникума')],
        [3, _('Не работаете по состоянию здоровья, инвалид')],
        [4, _('Пенсионер и не работаете')],
        [5, _('Находитесь в декретном отпуске')],
        [6, _('Находитесь в официальном отпуске по уходу за ребенком до 3 - х лет с сохранением места')],
        [7, _('Домашняя хозяйка, ухаживаете за другими членами семьи, воспитываете детей')],
        [8, _('Временно не работаете по другим причинам и ищете работу')],
        [9, _('Временно не работаете по другим причинам и не хотите работать')],
        [14, _('Другое')],
        HARD_TO_SAY_CHOICE
    ]

    MARITAL_STATUS_CHOICES = [
        [1, _('Не женаты/не замужем')],
        [2, _('Женаты/замужем')],
        [3, _('В отношениях, но официально не состоите в браке')],
        [4, _('Разведены')],
        [5, _('Живете отдельно от супруга/и')],
        [6, _('Вдовец/Вдова')],
        HARD_TO_SAY_CHOICE
    ]
    CITY_SIZE_CHOICES = [
        (1, '< 2,000'),
        (2, '2,000 - 5,000'),
        (3, '5,001- 10,000'),
        (4, '10,001 - 20,000'),
        (5, '20,001 - 50,000'),
        (6, '50,001 - 100,000'),
        (7, '100,001 - 500,000'),
        (8, '> 500,000'),
        (9, _('1 млн. и более')),
    ]
    LIVING_CHOICES = [
        [1, _('Жилье, находящееся в собственности у Вас и/или членов Вашей семьи    ')],
        [2, _('Государственное, муниципальное, ведомственное неприватизированное жилье')],
        [3, _('Арендованное жилье')],
        [4, _('Общежитие')],
        [5, _('Другое')]
    ]
    IncrementChoices5DNK = [
        [1, _('Безусловно увеличился')],
        [2, _('Скорее увеличился')],
        [3, _('Не изменился')],
        [4, _('Скорее уменьшился')],
        [5, _('Безусловно уменьшился')],
        HARD_TO_SAY_CHOICE,
    ]
    RELIGION_CHOICES = [
        [1, _('Не исповедую никакой религии (атеист)')],
        [2, _('Католицизм')],
        [3, _('Протестантизм')],
        [4, _('Православие')],
        [5, _('Иудаизм')],
        [6, _('Ислам')],
        [7, _('Индуизм')],
        [8, _('Буддизм')],
        [9, _('Другую религию')]
    ]
    SAME_MORAL_CHOICES = [
        [1, _('Совершенно согласен')],
        [2, _('Скорее согласен')],
        [3, _('Скорее не согласен')],
        [4, _('Совершенно не согласен')],
        HARD_TO_SAY_CHOICE,
        [6, _('Без ответа, я атеист')]
    ]
    CHURCH_ATTENDANCE_CHOICES = [
        [0, _('Вообще не бываю')],
        [1, _('1 раз в месяц или реже')],
        [2, _('2-3 раза в месяц')],
        [3, _('4 раза в месяц или чаще')],
        HARD_TO_SAY_CHOICE,
        [5, _('Без ответа, я атеист')]
    ]
    JUSTIFIED_CHOICES = range(1, 11)
    RISK_CHOICES = range(0, 11)
    AGREEMENT_CHOICES = [
        [1, _('Безусловно согласия, сплоченности')],
        [2, _('Скорее согласия, сплоченности')],
        [3, _('Скорее несогласия, разобщенности')],
        [4, _('Безусловно несогласия, разобщенности')],
        HARD_TO_SAY_CHOICE
    ]
    SIMILAR_TRUST_CHOICES = [
        [1, _('Безусловно больше')],
        [2, _('Скорее больше')],
        [3, _('Одинаково')],
        [4, _('Скорее меньше')],
        [5, _('Безусловно меньше')],
        HARD_TO_SAY_CHOICE
    ]
    SELF_TRUST_CHOICES = [
        [1, _('Вы доверчивы')],
        [2, _('Вы скорее доверчивы чем нет')],
        [3, _('Вы бываете и доверчивы и недоверчивы')],
        [4, _('Вы скорее недоверчивы')],
        [5, _('Вы недоверчивы')],
        HARD_TO_SAY_CHOICE
    ]
    READY_HELP_CHOICES = [
        [1, _('Да')],
        [2, _('Скорее да чем нет')],
        [3, _('Скорее нет чем да')],
        [4, _('Нет')],
        HARD_TO_SAY_CHOICE
    ]
    FEATURE_CHOICES = range(0, 11)
    FEATURE_CHOICES_1_10 = range(1, 11)
    SEPARATION_POWER_CHOICES = [
        [1, _('Разделение властей существует, система сдержек и противовесов реально работает')],
        [2, _('Разделение властей существует, несмотря на отдельные попытки нарушить систему сдержек и противовесов')],
        [3, _('Разделение властей существует формально, на практике система сдержек и противовесов работает плохо')],
        [4, _('Разделения властей нет, система сдержек и противовесов не работает')],
        HARD_TO_SAY_CHOICE

    ]
    INDEPENDENT_JUD_CHOICES = [
        [1, _('Суды независимы от других общественных институтов и некоррумпированы')],
        [2,
         _(
             'Суды в основном независимы, хотя иногда подвержены воздействию других общественных институтов и бывают случаи коррупции')],
        [3,
         _(
             'Независимость судов в значительной степени подорвана: они находятся во влиянием других общественных институтов и коррупции')],
        [4, _('Независимых судов в нашей стране нет')],
        HARD_TO_SAY_CHOICE

    ]
    CORRUPTION_CHOICES = [
        [1, _('Коррупция строго преследуется в соответствии с законом и подвергается публичному осуждению')],
        [2,
         _(
             'Коррупция в целом преследуется по закону и осуждается, однако иногда вовлеченным в нее людям удается найти лазейки и уйти от ответственности')],
        [3, _('Коррупция недостаточно преследуется по закону, и иногда подвергается публичному осуждению')],
        [4, _('Коррупция практически безнаказанна, и не осуждается публично')],
        HARD_TO_SAY_CHOICE
    ]
    CIVIL_RIGHTS_CHOICES = [
        [1, _('Гражданские права эффективно защищены законом, а их нарушение карается')],
        [2,
         _(
             'Гражданские права охраняются законом, но защита недостаточна, и нарушение этих прав не всегда преследуется')],
        [3,
         _(
             'Гражданские права обозначены в законе, но на практике нарушаются, и механизмы их защиты, как правило, неэффективны')],
        [4, _('Гражданские права систематически нарушаются, и механизмы их защиты отсутствуют')],
        HARD_TO_SAY_CHOICE
    ]
    SATIS_CHOICES = range(0, 11)
    HAPPY_CHOICES = [
        [0, _('Несчастливый человек')],
        [1, _('Счастливый человек')],
    ]
    RELATIVE_HAPPY_CHOICES = [
        [1, _('1 - Менее счастливы чем они')],
        [2, '2'],
        [3, '3'],
        [4, _('4 - В среднем так же счастлив, как и они')],
        [5, '5'],
        [6, '6'],
        [7, _('7 - Более счастлив чем они')]
    ]
    INCOME_CHOICES = [
        [1, _('Не хватает денег даже на еду')],
        [2, _('Хватает на еду, но не хватает на покупку одежды и обуви')],
        [3, _('Хватает на одежду и обувь, но не хватает на покупку мелкой бытовой техники')],
        [4,
         _(
             'Хватает денег на небольшие покупки, но покупка дорогих вещей (компьютера, стиральной машины, холодильника) требует накоплений или кредита')],
        [5,
         _(
             'Хватает денег на покупки для дома, но на покупку машины, дачи, квартиры необходимо копить или брать кредит')],
        [6, _('Можем позволить себе любые покупки без ограничений и кредитов')]
    ]
    PARTY_CHOICES = [
        [1, _('Единая Россия')],
        [2, _('КПРФ')],
        [3, _('ЛДПР')],
        [4, _('Справедливая Россия')],
        [5, _('Яблоко')],
        [6, _('Другая партия')],
        [7, _('В России нет партии, которой  я симпатизирую')],
        [8, _('Я не интересуюсь политикой')],
        HARD_TO_SAY_CHOICE
    ]
    AgreementChoices4DNK = [
        [1, _('Совершенно согласен')],
        [2, _('Скорее согласен')],
        [3, _('Скорее не согласен')],
        [4, _('Совершенно не согласен')],
        HARD_TO_SAY_CHOICE
    ]

    TrustChoices4DNK = [
        [1, _('Полностью доверяю')],
        [2, _('В некоторой степени доверяю')],
        [3, _('Не очень доверяю')],
        [4, _('Совсем не доверяю')],
        HARD_TO_SAY_CHOICE
    ]

    SimilarChoices6DNK = [
        [1, _('Очень похож на меня')],
        [2, _('Похож на меня')],
        [3, _('Отчасти похож на меня')],
        [4, _('Немного похож на меня')],
        [5, _('Не похож на меня')],
        [6, _('Совсем не похож на меня')],
    ]

    AgreementChoices5DNK = [
        [1, _('Совершенно согласен')],
        [2, _('Скорее согласен')],
        [3, _('И да и нет')],
        [4, _('Скорее не согласен')],
        [5, _('Совершенно не согласен')],
        HARD_TO_SAY_CHOICE
    ]

    Sibling4 = [
        [1, _('0')],
        [2, _('1')],
        [3, _('2')],
        [4, _('3')],
        [5, _('4 или более')],
    ]

    Region6 = [
        [1, _('0')],
        [2, _('1')],
        [3, _('2-3')],
        [4, _('4-6')],
        [5, _('7 или более')],
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
        [0, _('Я живу/жил/посещал этот регион')],
        [1, _('От родственников и друзей')],
        [2, _('Из социальных сетей (vk, instagram и др.)')],
        [3, _('Из средств массовой информации (газеты, телевидение, интернет-медиа и др.)')],
        [4, _('В школе или университете')],
        [5, _('Другие источники')],
        [999, _('Ничего не знаю о регионе')],
    ]
    BEEN_CHOICES = [
        [0, _('Да')],
        [1, _('Нет')],
    ]


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.payoff = 15
            p.participant.vars[_('questionnaire_payoff')] = p.payoff.to_real_world_currency(self.session)


class Group(BaseGroup):
    pass


class Player(BasePlayer):


    # Motivation
    motivation_part1 = models.TextField(
        label=_("""Пожалуйста, вспомните ваши решения в части 1 эксперимента.
            Участник А: передать ли начальную сумму участнику В.
            Участник В: ничего не возвращать, вернуть все или вернуть лишь часть 30 токенов
            Чем Вы руководствовались, принимая эти решения?
            Почему Вы решили именно так?""")
    )

    motivation_part2 = models.TextField(
        label=_("""Пожалуйста, вспомните ваши решения в части 2 эксперимента.
            Участник А: оценить, какую часть 30 токенов участник В захочет вернуть.
            Участник В: оценить, хотел ли участник А передать Вам его начальную сумму.
            Чем Вы руководствовались, принимая эти решения?
            Почему Вы решили именно так?""")
    )

    gender = models.BooleanField(initial=None,
                                 choices=Constants.GENDER_CHOICES,
                                 label=_('Ваш пол'),
                                 widget=widgets.RadioSelect())
    education = models.IntegerField(initial=None,
                                    choices=Constants.EDUCATION_CHOICES,
                                    label=_(
                                        """Какой у Вас самый высокий уровень образования, по которому Вы получили аттестат, свидетельство, диплом? """),
                                    widget=widgets.RadioSelect())
    occupation_status = models.IntegerField(initial=None,
                                            blank=True,
                                            choices=Constants.OCCUPATION_STATUS_CHOICES,
                                            label=_(
                                                """Какой ответ лучше всего описывает Ваше основное занятие в настоящее время?"""),
                                            widget=OtherRadioSelect(other=(14, _('occupation_status_other'))))
    occupation_status_other = models.CharField(blank=True,
                                               label=_("""Уточните какое именно""")
                                               )
    age = models.PositiveIntegerField(label=_('Ваш возраст (полных лет)'),
                                      min=13, max=95,
                                      initial=None)

    birthplace = models.CharField(
        label=_("""Место рождения (населенный пункт, регион)""")
    )

    marital_status = models.PositiveIntegerField(
        label=_('Ваш семейный статус'),
        choices=Constants.MARITAL_STATUS_CHOICES,
        widget=widgets.RadioSelect()
    )

    language = models.BooleanField(
        label=_('На каком языке Вы обычно говорите дома?'),
        choices=[
            [0, _('Русский')],
            [1, _('Другой (какой именно)')]
        ],
        widget=OtherRadioSelect(other=(1, _('language_other')))
    )

    language_other = models.CharField(blank=True,
                                      label=_("""Если на другом языке, то на каком именно?""")
                                      )

    living = models.PositiveIntegerField(
        label=_('Жильё (квартира, дом), в котором Вы живёте в настоящее время, это'),
        choices=Constants.LIVING_CHOICES,
        widget=OtherRadioSelect(other=(5, _('living_other')))
    )

    living_other = models.CharField(blank=True,
                                    label=_("""Уточните какое именно""")
                                    )

    city_size = models.PositiveIntegerField(
        label=_(
            """    Сколько человек (приблизительно) проживало в том населенном пункте, где Вы жили в возрасте 16 лет?"""),
        choices=Constants.CITY_SIZE_CHOICES,
        widget=widgets.RadioSelect())

    # Self-Determination

    ethnicity = models.IntegerField(
        label=_("""К какой национальности Вы себя относите?"""),
        choices=Constants.ETHNICITY_CHOICES,
        widget=OtherRadioSelect(other=(2, _('ethnicity_other')))
    )
    ethnicity_other = models.CharField(
        label=_("""Укажите к какой"""), blank=True
    )

    religion = models.PositiveIntegerField(
        label=_('Какую религию Вы исповедуете?'),
        choices=Constants.RELIGION_CHOICES,
        widget=OtherRadioSelect(other=(9, _('religion_other')))
    )

    religion_other = models.CharField(blank=True,
                                      label=_("""Уточните какую именно""")
                                      )

    religion_moral = models.PositiveIntegerField(
        label=_("""Насколько Вы согласны со следующим утверждением? "Люди, исповедующие другие религии, вероятно, 
        такие же глубоко моральные люди, как и те, что исповедуют Вашу религию."""),

        choices=Constants.SAME_MORAL_CHOICES,
        widget=widgets.RadioSelect(),
        blank=True
    )

    religion_service = models.PositiveIntegerField(
        label=_("""Как часто Вы посещаете храм"""),
        choices=Constants.CHURCH_ATTENDANCE_CHOICES,
        widget=widgets.RadioSelect(),
        blank=True
    )

    community_local = models.PositiveIntegerField(
        label=_("""Я считаю себя членом местной общины (сообщества) жителей моего города"""),
        choices=Constants.Agree4DNK
    )

    community_russian = models.PositiveIntegerField(
        label=_("""Я считаю себя россиянином"""),
        choices=Constants.Agree4DNK
    )

    # Trust

    general_trust = models.PositiveIntegerField(
        label=_("""Как Вы считаете, в целом большинству людей можно доверять, или же при общении с другими людьми 
            осторожность никогда не повредит?"""),
        choices=[
            [2, _("Нужно быть очень осторожным с другими людьми")],
            [1, _("Большинству людей можно вполне доверять")],
        ],
        widget=widgets.RadioSelect()
    )

    trust_family = models.IntegerField(
        label=_("""Ваша семья"""),
        choices=Constants.Trust4DNK,
        widget=widgets.RadioSelectHorizontal
    )
    trust_neighbours = models.IntegerField(
        label=_("""Ваши соседи"""),
        choices=Constants.Trust4DNK,
        widget=widgets.RadioSelectHorizontal
    )
    trust_acquant = models.IntegerField(
        label=_("""Люди, с которыми Вы лично знакомы"""),
        choices=Constants.Trust4DNK,
        widget=widgets.RadioSelectHorizontal
    )
    trust_stranger = models.IntegerField(
        label=_("""Люди, с которыми Вы не знакомы"""),
        choices=Constants.Trust4DNK,
        widget=widgets.RadioSelectHorizontal
    )
    trust_other_faith = models.IntegerField(
        label=_("""Люди другой веры"""),
        choices=Constants.Trust4DNK,
        widget=widgets.RadioSelectHorizontal
    )
    trust_fiends = models.IntegerField(
        label=_("""Ваши друзья"""),
        choices=Constants.Trust4DNK,
        widget=widgets.RadioSelectHorizontal
    )
    trust_politicians = models.IntegerField(
        label=_("""Политики"""),
        choices=Constants.Trust4DNK,
        widget=widgets.RadioSelectHorizontal
    )

    trust_church = models.IntegerField(
        label=_("""Церковь"""),
        choices=Constants.Trust4DNK
    )
    trust_army = models.IntegerField(
        label=_("""Армия"""),
        choices=Constants.Trust4DNK
    )
    trust_press = models.IntegerField(
        label=_("""Пресса (печатные медиа)"""),
        choices=Constants.Trust4DNK
    )
    trust_tv = models.IntegerField(
        label=_("""Телевидение"""),
        choices=Constants.Trust4DNK
    )
    trust_tradeunion = models.IntegerField(
        label=_("""Профсоюзы"""),
        choices=Constants.Trust4DNK
    )
    trust_police = models.IntegerField(
        label=_("""Полиция"""),
        choices=Constants.Trust4DNK
    )
    trust_courts = models.IntegerField(
        label=_("""Суды"""),
        choices=Constants.Trust4DNK
    )
    trust_government = models.IntegerField(
        label=_("""Правительство России"""),
        choices=Constants.Trust4DNK
    )
    trust_parties = models.IntegerField(
        label=_("""Политические партии"""),
        choices=Constants.Trust4DNK
    )
    trust_president = models.IntegerField(
        label=_("""Президент"""),
        choices=Constants.Trust4DNK
    )
    trust_parliament = models.IntegerField(
        label=_("""Парламент России"""),
        choices=Constants.Trust4DNK
    )
    trust_regional_authorities = models.IntegerField(
        label=_("""Региональная власть"""),
        choices=Constants.Trust4DNK
    )
    trust_local_authorities = models.IntegerField(
        label=_("""Местная власть"""),
        choices=Constants.Trust4DNK
    )
    trust_charity = models.IntegerField(
        label=_("""Гуманитарные и благотворительные организации"""),
        choices=Constants.Trust4DNK
    )
    trust_CIS = models.IntegerField(
        label=_("""Содружество независимых государств (СНГ)"""),
        choices=Constants.Trust4DNK
    )
    trust_UN = models.IntegerField(
        label=_("""Организация объединенных наций (ООН)"""),
        choices=Constants.Trust4DNK
    )

    dtrust = models.IntegerField(
        label=_(
            'По Вашему мнению, за последние годы изменился или не изменился уровень доверия людей друг к другу? Если изменился, то увеличился или уменьшился?'),
        choices=Constants.Inc5DNK,
        widget=widgets.RadioSelect()
    )

    # Values

    similar_newideas = models.IntegerField(
        label=_("""Для этого человека важно предлагать новые идеи, быть творческой личностью, идти своим путем"""),
        choices=Constants.Similar6DNK
    )

    similar_wealthy = models.IntegerField(
        label=_("""Для этого человека важно быть богатым,  иметь много денег и дорогих вещей"""),
        choices=Constants.Similar6DNK
    )

    similar_safety = models.IntegerField(
        label=_("""Для этого человека важно жить в безопасности, избегать всего, что может сулить опасность"""),
        choices=Constants.Similar6DNK
    )

    similar_hedonic = models.IntegerField(
        label=_("""Для этого человека важно хорошо проводить время, баловать себя"""),
        choices=Constants.Similar6DNK
    )

    similar_renowned = models.IntegerField(
        label=_("""Для этого человека важно быть очень успешным, чтобы окружающие знали о его достижениях"""),
        choices=Constants.Similar6DNK
    )

    similar_adventurous = models.IntegerField(
        label=_(
            """Приключения и риск очень важны для этого человека, он стремится к жизни, полной захватывающих событий"""),
        choices=Constants.Similar6DNK
    )

    similar_correct = models.IntegerField(
        label=_(
            """Для этого человека важно всегда вести себя правильно, не совершать поступков, которые люди не одобрили """),
        choices=Constants.Similar6DNK
    )

    similar_care_environment = models.IntegerField(
        label=_("""Для этого человека важно заботиться об окружающей среде и природе"""),
        choices=Constants.Similar6DNK
    )

    similar_tradition = models.IntegerField(
        label=_("""Для этого человека важно следовать традициям и обычаям, принятым в его семье или религии"""),
        choices=Constants.Similar6DNK
    )

    similar_care_society = models.IntegerField(
        label=_("""Для этого человека важно делать что-то хорошее для общества."""),
        choices=Constants.Similar6DNK
    )

    similar_care_nearby = models.IntegerField(
        label=_("""Для этого человека важно  заботиться о близких ему людях"""),
        choices=Constants.Similar6DNK
    )

    justified_subsidies = models.IntegerField(
        label=_("""Получение государственных пособий, на которые у человека нет права"""),
        choices=Constants.JUSTIFIED_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    justified_freeride = models.IntegerField(
        label=_("""Проезд без оплаты в общественном транспорте"""),
        choices=Constants.JUSTIFIED_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    justified_theft = models.IntegerField(
        label=_("""Кража чужой собственности"""),
        choices=Constants.JUSTIFIED_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    justified_tax_evasion = models.IntegerField(
        label=_("""Неуплата налогов, если есть такая возможность"""),
        choices=Constants.JUSTIFIED_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    justified_corruption = models.IntegerField(
        label=_("""Получение взятки"""),
        choices=Constants.JUSTIFIED_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    justified_violence = models.IntegerField(
        label=_("""Применение насилия в отношении других людей"""),
        choices=Constants.JUSTIFIED_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    # Risk
    risk_general = models.PositiveIntegerField(
        label='',
        choices=Constants.RISK_CHOICES,
        widget=LikertWidget(
            quote=_(
                "Укажите, пожалуйста, насколько Вы в целом любите рисковать?"),
            label=_(
                """Для ответа выберите значение на шкале от 0 до 10, где  0 означает, что Вы «совершенно не готовы рисковать»,
                 а 10 означает, что Вы «охотно идете на риск».
                """),
            left=_('Я совершенно не готов рисковать'),
            right=_('Я охотно иду на риск'),
        )
    )

    risk_fin = models.PositiveIntegerField(
        label=_("""В финансовых вопросах"""),
        choices=Constants.RISK_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    risk_sport = models.PositiveIntegerField(
        label=_("""В свободное время и во время занятий спортом"""),
        choices=Constants.RISK_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    risk_prof = models.PositiveIntegerField(
        label=_("""В вашей профессии"""),
        choices=Constants.RISK_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    risk_health = models.PositiveIntegerField(
        label=_("""В том что касается вашего здоровья"""),
        choices=Constants.RISK_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    risk_strangers = models.PositiveIntegerField(
        label=_("""В отношениях с незнакомыми людьми"""),
        choices=Constants.RISK_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )
    risk_drive = models.PositiveIntegerField(
        label=_("""Во время езды за рулем"""),
        choices=Constants.RISK_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    # StatedPreferences
    moreagreement = models.PositiveIntegerField(
        label=_(
            """Как Вы думаете, сегодня в нашей стране среди людей больше согласия, сплоченности или несогласия, разобщенности?"""),
        choices=Constants.AGREEMENT_CHOICES,
        widget=widgets.RadioSelect()
    )

    similar_trust = models.PositiveIntegerField(
        label=_(
            """Людям, с которыми у Вас много общего, Вы доверяете больше, чем всем остальным, меньше чем остальным или же одинаково?"""),
        choices=Constants.SIMILAR_TRUST_CHOICES,
        widget=widgets.RadioSelect()
    )

    trustful = models.PositiveIntegerField(
        label=_("""Можете ли Вы сказать о себе, что Вы доверчивый человек?"""),
        choices=Constants.SELF_TRUST_CHOICES,
        widget=widgets.RadioSelect()
    )

    ready_help = models.PositiveIntegerField(
        label=_(
            """Готовы ли Вы тратить свои ресурсы на благое дело, даже если не рассчитываете ничего получить взамен?"""),
        choices=Constants.READY_HELP_CHOICES,
        widget=widgets.RadioSelect()
    )

    dreadyhelp = models.IntegerField(
        label=_(
            'По Вашему мнению, за последние годы изменился или не изменился уровень готовности людей помогать друг другу? Если изменился, то увеличился или уменьшился?'),
        choices=Constants.Inc5DNK,
        widget=widgets.RadioSelect()
    )

    freedom = models.PositiveIntegerField(
        label=(""),
        choices=Constants.FEATURE_CHOICES_1_10,
        widget=LikertWidget(
            quote=_(
                """Некоторые люди чувствуют, что они обладают полной свободой выбора и контролируют свою жизнь, в
         то время как другие люди чувствуют, что то, что они делают, не имеет реального влияния на происходящее с ними. 
         До какой степени эти характеристики применимы к Вам и Вашей жизни?"""),
            label=_(
                """Для ответа выберите значение на шкале от 1 до 10, где 1 означает "у меня нет свободы выбора", а 10
         означает "у меня полная свобода выбора.
                """),
            left=_('У меня нет свободы выбора'),
            right=_('У меня полная свобода выбора'),
        )
    )
    competition = models.PositiveIntegerField(
        label=(""),

        choices=Constants.FEATURE_CHOICES_1_10,
        widget=LikertWidget(
            quote=_(
                "Как Вы думаете, конкуренция - это зло или благо?"),
            label=_(
                """Для ответа выберите значение на шкале от 1 до 10, где 1 означает, что «конкуренция вредна, 
                поскольку она побуждает у людей худшие качества»,
             а 10 означает, что «конкуренция - это благо, поскольку она побуждает людей лучше трудиться»
                """),
            left=_('Конкуренция вредна, поскольку она побуждает у людей худшие качества'),
            right=_('Конкуренция - это благо, поскольку она побуждает людей лучше трудиться'),
        )
    )

    fairness_general = models.PositiveIntegerField(
        label='',
        choices=Constants.FEATURE_CHOICES_1_10,
        widget=LikertWidget(
            quote=_(
                'Как Вы думаете, могут ли люди в современном обществе разбогатеть только за счет других людей, или уровень благосостояния может вырасти у всех?'),
            label=_(
                'Для ответа выберите значение на шкале от 1 до 10, где 1 означает, что «люди могут разбогатеть только за счет других», а 10 означает, что «благосостояние может вырасти у всех»'),
            left=_('Люди могут разбогатеть только за счет других'),
            right=_('Благосостояние может вырасти у всех'),
        )
    )

    positive_reciprocity = models.PositiveIntegerField(
        label=(""),
        choices=Constants.FEATURE_CHOICES,
        widget=LikertWidget(
            quote=_(
                "\"Когда кто-либо мне помогает я стараюсь ответить тем же.\"  Справедливо ли это суждение в отношении Вас?"),
            label=_(
                """Для ответа выберите значение на шкале от 0 до 10,
         где 0 означает, что Вы «совершенно не готовы так поступать», а 10 означает, что Вы «готовы поступать именно так»"""
            ),
            left=_('Я совершенно не готов так поступать'),
            right=_('Я готов поступать именно так'),
        )
    )

    negative_reciprocity = models.PositiveIntegerField(
        label='',
        choices=Constants.FEATURE_CHOICES,
        widget=LikertWidget(
            quote=_(
                """"Если со мной поступили несправедливо, я отомщу при первом же удобном случае,
                даже если это дорого мне обойдется."  Справедливо ли это суждение в отношении Вас?
                """
            ),
            label=_(
                """Для ответа выберите значение на шкале от 0 до 10,
          где 0 означает, что Вы «совершенно не готовы так поступать», а 10 означает, что Вы «готовы поступать именно так»
                """
            ),
            left=_('Я совершенно не готов так поступать'),
            right=_('Я готов поступать именно так'),
        )
    )

    abuse_you = models.PositiveIntegerField(
        label=(''),
        choices=Constants.FEATURE_CHOICES,
        widget=LikertWidget(
            quote=_(
                'Как Вы думаете, если представится возможность, большинство людей попытались бы использовать вас в своих интересах, или вели бы себя порядочно?'),
            label=_(
                'Для ответа выберите значение на шкале от 0 до 10, где 0 означает, что «люди обязательно попытаются вас использовать», а 10 означает, что «люди поведут себя порядочно»'),
            left=_('Люди обязательно попытаются вас использовать'),
            right=_('Люди поведут себя порядочно'),
        )
    )

    fairness_russian = models.PositiveIntegerField(
        label=_("""Социальные различия между людьми в нашей стране в целом оправданны и справедливы"""),
        choices=Constants.Agree5DNK,
        widget=widgets.RadioSelect()
    )
    separation_power = models.PositiveIntegerField(
        label=_(
            """Как Вы считаете, в нашей стране сейчас имеет место разделение властей (законодательной, исполнительной и судебной) или же нет?"""),
        choices=Constants.SEPARATION_POWER_CHOICES,
        widget=widgets.RadioSelect()
    )

    independent_judiciary = models.PositiveIntegerField(
        label=_("""Как Вы считаете, независимы ли в нашей стране суды?"""),
        choices=Constants.INDEPENDENT_JUD_CHOICES,
        widget=widgets.RadioSelect()
    )

    corruption = models.PositiveIntegerField(
        label=_("""Что Вы думаете про борьбу с коррупцией в нашей стране?"""),
        choices=Constants.CORRUPTION_CHOICES,
        widget=widgets.RadioSelect()
    )

    civil_rights = models.PositiveIntegerField(
        label=_("""До какой степени у нас в стране защищены гражданские права?"""),
        choices=Constants.CIVIL_RIGHTS_CHOICES,
        widget=widgets.RadioSelect()
    )

    Ark_been = models.BooleanField(
        label=_("""Архангельск и Архангельская область"""),
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Vlk_been = models.BooleanField(
        label=_("""Владивосток и Приморский край"""),
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Vor_been = models.BooleanField(
        label=_("""Воронеж и Воронежская область"""),
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Ekb_been = models.BooleanField(
        label=_("""Екатеринбург и Свердловская область"""),
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Kaz_been = models.BooleanField(
        label=_("""Казань и республика Татарстан"""),
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Mak_been = models.BooleanField(
        label=_("""Махачкала и республика Дагестан"""),
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Mos_been = models.BooleanField(
        label=_("""Москва"""),
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Nsk_been = models.BooleanField(
        label=_("""Новосибирск и Новосибирская область"""),
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Per_been = models.BooleanField(
        label=_("""Пермь и Пермский край"""),
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Ros_been = models.BooleanField(
        label=_("""Ростов-на-Дону и Ростовская область"""),
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    SPb_been = models.BooleanField(
        label=_("""Санкт-Петербург"""),
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Khb_been = models.BooleanField(
        label=_("""Харабовск и Хабаровский край"""),
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    abroad_been = models.BooleanField(
        label=_("""Бывали ли Вы когда-либо за границей?"""),
        choices=Constants.BEEN_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    Ark_source = models.StringField(
        widget=BlockedCheckbox(choices=Constants.SOURCE_CHOICES, blocked=999,
                               label=_("""Архангельск и Архангельская область"""))
    )

    Vlk_source = models.StringField(

        widget=BlockedCheckbox(choices=Constants.SOURCE_CHOICES, blocked=999,
                               label=_("""Владивосток и Приморский край"""),
                               )
    )

    Vor_source = models.StringField(

        widget=BlockedCheckbox(choices=Constants.SOURCE_CHOICES, blocked=999,
                               label=_("""Воронеж и Воронежская область"""),
                               )
    )

    Ekb_source = models.StringField(

        widget=BlockedCheckbox(choices=Constants.SOURCE_CHOICES, blocked=999,
                               label=_("""Екатеринбург и Свердловская область"""),
                               )
    )

    Kaz_source = models.StringField(

        widget=BlockedCheckbox(choices=Constants.SOURCE_CHOICES, blocked=999,
                               label=_("""Казань и республика Татарстан"""),
                               )
    )

    Mak_source = models.StringField(

        widget=BlockedCheckbox(choices=Constants.SOURCE_CHOICES, blocked=999,
                               label=_("""Махачкала и республика Дагестан"""),
                               )
    )

    Mos_source = models.StringField(
        label=_("""Москва"""),
        widget=BlockedCheckbox(choices=Constants.SOURCE_CHOICES, blocked=999,
                               label=_("""Москва"""),
                               )
    )

    Nsk_source = models.StringField(
        widget=BlockedCheckbox(choices=Constants.SOURCE_CHOICES, blocked=999,
                               label=_("""Новосибирск и Новосибирская область"""),
                               )
    )

    Per_source = models.StringField(

        widget=BlockedCheckbox(choices=Constants.SOURCE_CHOICES, blocked=999,
                               label=_("""Пермь и Пермский край"""),
                               )
    )

    Ros_source = models.StringField(

        widget=BlockedCheckbox(choices=Constants.SOURCE_CHOICES, blocked=999,
                               label=_("""Ростов-на-Дону и Ростовская область"""),
                               )
    )

    SPb_source = models.StringField(

        widget=BlockedCheckbox(choices=Constants.SOURCE_CHOICES, blocked=999,
                               label=_("""Санкт-Петербург"""), )
    )

    Khb_source = models.StringField(
        widget=BlockedCheckbox(choices=Constants.SOURCE_CHOICES, blocked=999,
                               label=_("""Харабовск и Хабаровский край"""))
    )
    relative_position_in_region = models.IntegerField(
        label=_('Ваш средний ежемесячный доход'),
        choices=Constants.RELATIVE_POSITION_CHOICES,
        widget=widgets.RadioSelect()
    )
    Ark_rank = models.CharField(
        label=_("""Архангельск и Архангельская область""")
    )

    Vlk_rank = models.CharField(
        label=_("""Владивосток и Приморский край""")
    )

    Vor_rank = models.CharField(
        label=_("""Воронеж и Воронежская область""")
    )

    Ekb_rank = models.CharField(
        label=_("""Екатеринбург и Свердловская область""")
    )

    Kaz_rank = models.CharField(
        label=_("""Казань и республика Татарстан""")
    )

    Mak_rank = models.CharField(
        label=_("""Махачкала и республика Дагестан""")
    )

    Mos_rank = models.CharField(
        label=_("""Москва""")
    )

    Nsk_rank = models.CharField(
        label=_("""Новосибирск и Новосибирская область"""))

    Per_rank = models.CharField(
        label=_("""Пермь и Пермский край""")
    )

    Ros_rank = models.CharField(
        label=_("""Ростов-на-Дону и Ростовская область""")
    )

    SPb_rank = models.CharField(
        label=_("""Санкт-Петербург""")
    )

    Khb_rank = models.CharField(
        label=_("""Харабовск и Хабаровский край""")
    )
    rank_comment = models.LongStringField(label=_('Комментарий к вашему рейтингу'), blank=True)
    regional_income = models.CharField(
        label=_(
            """Как Вы считаете, каков среднемесячный доход жителей Вашего региона? Напишите пожалуйста Вашу оценку (в рублях в месяц)""")
    )

    regional_differences = models.PositiveIntegerField(
        label=_(
            """Согласны ли Вы с утверждением, что различия в уровне доходов между регионами России неоправданно велики"""),
        choices=Constants.Agree5DNK,
        widget=widgets.RadioSelect
    )

    satis = models.PositiveIntegerField(
        label="",
        choices=Constants.SATIS_CHOICES,
        widget=LikertWidget(
            quote=_(
                'Учитывая все обстоятельства, насколько Вы удовлетворены вашей жизнью в целом в эти дни?'),
            label=_(
                """ Для ответа выберите значение на шкале от 0 до 10, где 0 означает «совершенно не удовлетворен», а 10 - «полностью удовлетворен»)"""),
            left=_('Совершенно не удовлетворен'),
            right=_('Полностью удовлетворен'),
        )
    )

    happy = models.BooleanField(
        label=_("""В целом я могу сказать, что я"""),
        choices=Constants.HAPPY_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    happy_relative = models.PositiveIntegerField(
        label=_("""По сравнению с большинством окружающих вас людей, вы"""),
        choices=Constants.RELATIVE_HAPPY_CHOICES,
        widget=widgets.RadioSelect()
    )

    income = models.PositiveIntegerField(
        label=_("""Какое высказывание наиболее точно описывает финансовое положение вашей семьи?"""),
        choices=Constants.INCOME_CHOICES,
        widget=widgets.RadioSelect()
    )

    elder_sibling = models.PositiveIntegerField(
        label=_("""Сколько у вас старших братьев или сестер?"""),
        choices=Constants.Sib4
    )

    younger_sibling = models.PositiveIntegerField(
        label=_("""Сколько у вас младших братьев или сестер?"""),
        choices=Constants.Sib4
    )

    father_born = models.CharField(blank=True,
                                   label=_(
                                       """В каком регионе родился Ваш отец (если не знаете оставьте поле пустым)?"""),
                                   )

    mother_born = models.CharField(blank=True,
                                   label=_(
                                       """В каком регионе родилась Ваша мать (если не знаете оставьте поле пустым)?"""),
                                   )

    regions_been = models.PositiveIntegerField(
        label=_("""В скольких регионах России (не считая вашего) вам случалось бывать)?"""),
        choices=Constants.Reg6,
        widget=widgets.RadioSelectHorizontal
    )

    honest_Russia = models.PositiveIntegerField(
        label=_(
            """В нынешней России честному человеку трудно достичь каких-то высот, занять высокое положение в обществе"""),
        choices=Constants.Agree5DNK,
        widget=widgets.RadioSelect
    )

    party_Russia = models.PositiveIntegerField(
        label=_("""Сторонником какой политической партии вы являетесь, или по крайней мере,симпатизируете ей? """),
        choices=Constants.PARTY_CHOICES,
        widget=OtherRadioSelect(other=(6, _('party_other')))
    )

    party_other = models.CharField(blank=True,
                                   label=_("""Если Вы сторонник другой партии, укажите какой именно"""),
                                   )

    who_was_other_city = models.IntegerField(
        label=_("Как Вы думаете, с участником из какого города вы взаимодействовали в ходе этого исследования?"),
        choices=Constants.CITIES,
        widget=OtherRadioSelect(other=(13, _('who_was_other_city_other')))
    )
    who_was_other_city_other = models.CharField(
        label="", blank=True
    )

    def get_rank_fields(self):
        # not the best decision if someone adds other fields ending with _rank... thoough
        r = [dict(name=f.name, label=str(f.verbose_name)) for f in self._meta.get_fields() if
             f.name.endswith('_rank')]
        return r

    is_occupied = models.BooleanField(label=_("В настоящее время вы трудоустроены?"),
                                      choices=Constants.IS_OCCUPIED_CHOICES,
                                      widget=widgets.RadioSelectHorizontal)
    self_employed = models.BooleanField(label=_("Являетесь ли вы в настоящее время самозанятым?"),
                                        choices=Constants.IS_OCCUPIED_CHOICES,
                                        widget=widgets.RadioSelectHorizontal,
                                        blank=True)
    occupation_parent = models.IntegerField(choices=Constants.OCCUPATION_PARENT_CHOICES, blank=True)
    occupation_child = models.IntegerField(choices=Constants.OCCUPATION_CHILD_CHOICES, blank=True)
