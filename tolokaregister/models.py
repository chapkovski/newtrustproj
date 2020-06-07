from django.db import models
from otree.models import Participant
from enum import Enum
from .toloka import TolokaClient
import json

# Some constants - mostly temporarily
DEFAULT_BONUS_TITLE = 'Thanks!'
DEFAULT_BONUS_MESSAGE = 'Thank you for your participation'
"""
-  status (accept, reject, unknown, active, submitted, error)
- Info (just a dump for response based on label of initial participant),  
- assignment (=label by initial participant), 
- bonus_paid (flag/amount if bonus has been paid via otree interface). 
- bonus_amount-  total amount paid via interface
- answer_is_correct - compare the answer with the participant code
- answer
- bonus_is_calculated

"""
"""
RESPONSE EXAMPLE
"""
"""
SANDBOX ASSIGNMENT EXAMPLE 000005e173--5eb766016ce18f023c602691
{
    "id": "0000cba366--5eb5e222a8f57568f628784f",
    "task_suite_id": "0000cba366--5eb5e1f7cbef577b72d5b189",
    "pool_id": "13345638",
    "user_id": "326dd7a1de11772eca554c59cbcf13e7",
    "status": "ACCEPTED",
    "reward": 0.10,
    "tasks": [
        {
            "id": "b27a23f7-e3fa-49d3-a8d6-7fd0c8c41aff",
            "input_values": {
                "session_url": "https://stormy-chamber-12502.herokuapp.com/join/b4eedm5raj/"
            }
        }
    ],
    "solutions": [
        {
            "output_values": {
                "otree_code": "625fc7rf"
            }
        }
    ],
    "mixed": false,
    "automerged": false,
    "created": "2020-05-08T22:50:10.809",
    "submitted": "2020-05-08T22:50:54.934",
    "accepted": "2020-05-08T23:15:39.717",
    "owner": {
        "id": "e8272061e849238f597cb3c5e757ade7",
        "myself": true
    }
}
"""


class UpdParticipant(Participant):
    class Meta:
        proxy = True

    def __str__(self):
        return self.code

    def get_tp(self):
        try:
            r = self.tolokaparticipant
            return r
        except  TolokaParticipant.DoesNotExist as e:
            return False


class StatusEnum(Enum):
    unknown = 'UNKNOWN'
    submitted = 'SUBMITTED'
    accepted = 'ACCEPTED'
    rejected = 'REJECTED'
    active = 'ACTIVE'
    error = 'ERROR'


class TolokaParticipant(models.Model):
    """we don't need all these blank=true, only for debugging purposes so we can deal with this in admin"""
    owner = models.OneToOneField(to=UpdParticipant, on_delete=models.CASCADE,
                                 related_name='tolokaparticipant')
    status = models.CharField(max_length=1000, default=StatusEnum.unknown.value)
    info = models.TextField(null=True, blank=True)
    """The assginemnt is the only important thing here becuase it links otree and toloka together"""
    assignment = models.CharField(max_length=1000, unique=True)
    toloka_user_id = models.CharField(max_length=1000, null=True, blank=True)
    bonus_paid = models.BooleanField(null=True, blank=True)

    answer_is_correct = models.BooleanField(null=True, blank=True)
    answer = models.CharField(max_length=1000, null=True, blank=True)
    bonus_is_calculated = models.BooleanField(null=True, blank=True)
    sandbox = models.BooleanField()

    def __str__(self):
        return f'Participant {self.owner.code}; assignment {self.assignment}'

    @property
    def payable(self):
        return self.status == StatusEnum.accepted.value and not self.bonus_paid

    @property
    def acceptable(self):

        """Check if assignment can be accepted. Theoretically rejected assignmentes can be accepted, but we'll
        be naive and accept only submitted assignments - everything else can be dealt with in toloka interface"""
        return self.status == StatusEnum.submitted.value

    def update_info_from_toloka(self, resp):
        """given a resp from toloka, udpate instance properties. It is far from optimal, but just a bit simpler"""
        print("WHAT WE GET AS RESP?", resp)
        if not resp.get('error'):
            self.status = resp.status
            self.info = json.dumps(resp)
            self.toloka_user_id = resp.user_id
            if hasattr(resp, 'solutions') and isinstance(resp.solutions, list) and len(resp.solutions) > 0:
                self.answer = self.process_solutions(resp.solutions)
                self.answer_is_correct = self.check_answer()
        else:
            self.status = StatusEnum.error.value
            self.info = json.dumps(resp)
        self.save()

    def accept_assignment(self):
        """check if status is Submitted. and iif yes - send accept request to toloka, return positive response back.
        otherwise sends error=True back. use sandbox param to get info.
        Theoretically rejected assignments can be (re-) accepted, but I dont' want to deal with this mess.
        """
        if self.status == StatusEnum.submitted.value:
            client = TolokaClient(self.sandbox)
            resp = client.accept_assignment(self.assignment)
            self.status = resp.status
            self.save()
            return dict(error=False, **resp)  # send toloka accept request here
        else:
            return dict(error=True)

    def process_solutions(self, solutions):
        """get toloka solutions json and process it to retrieve nessesary answer.
        By default we retrieve otree_code from the first solution object, but it can be overriden later"""
        """
          "solutions": [
        {
            "output_values": {
                "otree_code": "625fc7rf"
            }
        }
    ],"""
        if len(solutions) > 0:
            first = solutions[0]
            try:
                return first.get('output_values').get('otree_code')
            except Exception as e:
                print(e)
                return False
        else:
            return False

    def check_answer(self):
        """This one assumes that the code provided in toloka should be equal to participant code.
        This assumption can be overrided later, that is why we move it into a separate function.
        """
        return self.answer == self.owner.code

    def get_info(self):
        """Do something here with toloka participant  -
           and then request in toloka the assignment status and return it back. In case of the error just return {error:true}
           and perhaps error message provided by toloka.use sandbox param to get info
           """
        try:
            """Send here to toloka request using assignment id. In case of success we disentangle the response and assign
            its different parts to TP instance """
            client = TolokaClient(self.sandbox)

            resp = client.get_assignment_info(self.assignment)
            self.update_info_from_toloka(resp)
            return dict(success=True)

        except Exception as e:  # let's capture some specific toloka errors TODO
            print(e)
            return dict(error=True)

    def pay_bonus(self):
        """iif status is accepted and bonus is paid is false then pay a bonus retrieved from bonus_to_pay"""
        if not self.bonus_paid:
            """send pay bonus request to toloka"""

            client = TolokaClient(self.sandbox)
            user_id = self.toloka_user_id
            bonus = float(self.owner.payoff_in_real_world_currency())
            # TODO:
            """We will customize these messages later """
            title = DEFAULT_BONUS_TITLE
            message = DEFAULT_BONUS_MESSAGE
            resp = client.pay_bonus(user_id, bonus, title, message)
            self.bonus_paid = True
            self.save()
            return dict(error=False, **resp)
        else:
            return dict(error=True, errmsg='Bonus already paid')
