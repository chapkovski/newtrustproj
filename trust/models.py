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
from django.db import models as djmodels
from django.conf import settings

author = 'Philipp Chapkovski'

doc = """
Interregional trust game. 
"""


class Constants(BaseConstants):
    name_in_url = 'trust'
    players_per_group = None
    num_rounds = 1
    sender_endowment = 10
    step = 3
    coef = 3
    sender_choices = ((0, 'No'), (sender_endowment, "Yes"))
    receiver_choices = list(range(0, sender_endowment*coef + 1, step))
    expanded_receiver_choices = list(zip(receiver_choices, receiver_choices))

class Subsession(BaseSubsession):
    matched_different = models.BooleanField(default=True)

    @property
    def cities(self):
        return set([self.session.config.get('city1'), self.session.config.get('city2')])

    def creating_session(self):
        if self.session.num_participants % 2 != 0:
            raise Exception('Number of participants should be even!')
        for i in settings.CITIES:
            City.objects.get_or_create(code=i['code'], defaults={'description': i['name']})

        if len(self.cities) != len(set(self.cities)): raise Exception('Вы ввели два одинаковых города! Не надо так.')
        registered_cities = set(City.objects.all().values_list('code', flat=True))
        if not set(self.cities).issubset(registered_cities):
            raise Exception('Вы ввели неверный код для одного из городов!')


class Group(BaseGroup):
    def set_payoffs(self):
        sender = self.get_player_by_role('Sender')
        receiver = self.get_player_by_role('Receiver')
        sender_city = City.objects.get(code=sender.city)
        receiver_city = City.objects.get(code=receiver.city)
        sender_decision_re_receiver = sender.senderdecisions.get(city=receiver_city).send
        receiver_decision_re_sender = receiver.returndecisions.get(city=sender_city).send_back
        sender.payoff = Constants.sender_endowment - sender_decision_re_receiver + receiver_decision_re_sender
        receiver.payoff = sender_decision_re_receiver * Constants.coef - receiver_decision_re_sender


class Player(BasePlayer):
    city = models.StringField()
    _role = models.StringField()

    def role(self):
        if not self._role:
            return 'Sender' if self.id_in_subsession % 2 == 1 else 'Receiver'
        else:
            return self._role

    def create_decisions(self):
        if self.role() == 'Sender':
            self.create_sender_decisions()
        else:
            self.create_receiver_decisions()

    def create_beliefs(self):
        if self.role() == 'Sender':
            self.create_sender_beliefs()
        else:
            self.create_receiver_beliefs()

    def create_sender_decisions(self):
        self._universal_creator(SenderDecision)

    def create_receiver_decisions(self):
        self._universal_creator(ReturnDecision)

    def create_sender_beliefs(self):
        self._universal_creator(SenderBelief)

    def create_receiver_beliefs(self):
        self._universal_creator(ReturnerBelief)

    def _universal_creator(self, obj):
        for city in City.objects.all():
            obj.objects.create(city=city, owner=self)


class City(djmodels.Model):
    code = models.StringField(unique=True)
    description = models.StringField(unique=True)

    def __str__(self):
        return f'Code: {self.code}; Description: {self.description}'


class Decision(djmodels.Model):
    city = djmodels.ForeignKey(to=City, on_delete=djmodels.CASCADE, null=True)
    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name="%(class)ss")

    class Meta:
        abstract = True
        unique_together = [['city', 'owner']]


class SenderDecision(Decision):
    send = models.IntegerField()


class ReturnDecision(Decision):
    send_back = models.IntegerField()


class SenderBelief(Decision):
    belief_on_return = models.IntegerField()


class ReturnerBelief(Decision):
    belief_on_send = models.IntegerField()
