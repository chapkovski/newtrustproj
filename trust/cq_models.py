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

from django.core.exceptions import ValidationError

correct_answers = dict(
    cq1_1=30,
    cq1_2=30,
    cq1_3=20,
    cq1_4=31,
    cq1_5=9,
    cq1_6=10,
    cq1_7=10,
    cq1_8=3,
    cq1_9=2,
    cq2_1=0,
    cq2_2=10,
    cq2_3=0,
    cq2_4=10,
    cq2_5=20,
)


class CQ(models.IntegerField):
    def internal_validator(self, value):
        if hasattr(self, 'correct_answer'):
            if value != correct_answers[self.correct_answer]:
                raise ValidationError(f'Please check this answer')


    def __init__(self, *args, **kwargs):
        if 'correct_answer' in kwargs:
            self.correct_answer = kwargs['correct_answer']

        kwargs['validators'] = [self.internal_validator]
        kwargs.pop('correct_answer', None)
        super().__init__(*args, **kwargs)


cq_1_8_choices = ((1, 'None'),
                  (2, '12 - one per each city that is involved in this study.'),
                  (3, '1 - a randomly chosen participant from one of the 12 cities that are involved in this study. '))
cq_1_9_choices = ((1, '12 - one per each city that is involved in this study.'),
                  (2, '1 - a randomly chosen participant from one of the 12 cities that are involved in this study. '),
                  (3, 'None')
                  )


class CQPlayer(BasePlayer):
    class Meta:
        abstract = True

    # cqs for part 1
    cq1_1 = CQ(label='If Person A transfers his initial endowment to Person B, how many token does Person B receive? ',
               correct_answer='cq1_1')
    cq1_2 = CQ(
        label='A Person A transfers his initial endowment to Person B. What is the maximum amount Person B can return to Person A? ',
        correct_answer='cq1_2')
    cq1_3 = CQ(label='Person B decides to return to Person A 20 points. How many points does Person A receive from this transfer?',
               correct_answer='cq1_3')
    cq1_4 = CQ(
        label='What is the payoff of Person B if Person A transfers his initial endowment and Person B sends back 9 points?'
        , correct_answer='cq1_4')
    cq1_5 = CQ(
        label='What is the payoff of Person A if he transfers his initial endowment and Person B sends him back 9 points?',
        correct_answer='cq1_5')
    cq1_6 = CQ(
        label='What is the payoff of Person A if Person A decides NOT to transfer his initial endowment to Person B? ',
        correct_answer='cq1_6')
    cq1_7 = CQ(
        label='What is the payoff of Person B if Person A decides NOT to transfer his initial endowment to Person B? ',
        correct_answer='cq1_7')
    cq1_8 = CQ(
        label='Imagine you have been randomly assigned to be Person A. For how many participants in the role of Person B your decision to transfer or not transfer your initial endowment will be payoff relevant?',
        choices=cq_1_8_choices, correct_answer='cq1_8', widget=widgets.RadioSelect)
    cq1_9 = CQ(
        label='Imagine you have been randomly assigned to be Person B. How many participants in the role of Person A will decide on whether you actually receive a multiplied initial endowment?',
        choices=cq_1_9_choices, correct_answer='cq1_9', widget=widgets.RadioSelect)

    # cqs for part 1
    cq2_1 = CQ(
        label=' If Person A from City 1 transferred his initial endowment, while the estimate of Person B was that a person from City 1 will not transfer the endowment, what will be the payoff of Person B for Part 2? ',
        correct_answer='cq2_1')
    cq2_2 = CQ(
        label='If Person A from City 1 transferred his initial endowment. Person B’s estimate for a Person A from City 1 was that this person transfers his endowment. What will be the payoff of Person B for Part 2?',
        correct_answer='cq2_2')
    cq2_3 = CQ(
        label='In Part 1, a Person A from City 1 transferred his initial endowment to a Person B from City 2. Person B returns 15 tokens to Person A in Part 1. In Part 2, Person A estimated that Person B returns 9 tokens.  What will be the payoff of Person A for Part 2? ',
        correct_answer='cq2_3')
    cq2_4 = CQ(
        label=' In Part 1, a Person A from City 1 did not transfer his initial endowment to a Person B from City 2. Person B from City 2 chose to return 15 tokens to Person A if Person A transfers his initial endowment. In Part 2, Person A estimated that Person B would return 18 tokens.  What will be the payoff of Person A for Part 2?',
        correct_answer='cq2_4')
    cq2_5 = CQ(
        label='In Part 1, a Person A from City 1 transferred his initial endowment to a Person B from City 2. Person B from City 2 chose to return 0 tokens to Person A if Person A transfers his initial endowment. In Part 2, Person A estimated that Person B would return 0 tokens. What will be the payoff of Person A for Part 2?',
        correct_answer='cq2_5')
