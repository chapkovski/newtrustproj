"""
Contains models for mingling sessions into larger megasessions, plus some 1to1 to Participant model
"""
from otree.models import Participant, Session
from django.db import models
import random


class MingleSession(models.Model):
    """1to1 to prevent double mingling. This is basically the linkage between otree sessions and megasessions"""
    owner = models.OneToOneField(to=Session, on_delete=models.CASCADE, related_name='minglesession')
    megasession = models.ForeignKey(to='MegaSession', on_delete=models.SET_NULL, related_name='minglesessions',
                                    null=True, blank=True)


class MegaSession(models.Model):
    """Container for all sessions belonging to one mega. It is also container for participants and megagroups."""
    comment = models.CharField(max_length=1000, null=True, blank=True)
    payoff_calculated = models.BooleanField(default=False)
    groups_formed = models.BooleanField(default=False)

    def __str__(self):
        return f'Wrapper for {self.minglesessions.all().count()}'

    def form_groups(self):
        """That takes all megaparticipants and create groups from the randmo pairs"""
        if self.payoff_calculated:
            return
        parts = self.megaparticipants.all()
        assert (parts.count() % 2 == 0, 'Number of participants is odd!')
        parts = list(parts)
        random.shuffle(parts)
        chunked = [parts[i:i + 2] for i in range(0, len(parts), 2)]
        for g in chunked:
            newg = MegaGroup.objects.create(megasession=self)
            for p in g:
                p.group = newg
                p.save()

        print('CHUNKED', chunked)

    def calculate_payoffs(self):
        """loop over all groups and make payoff calculations"""
        if self.payoff_calculated:
            return


class MegaParticipant(models.Model):
    """1to1 link to participant for freezing those whose payoffs were calculated.
    Not really necessary but maybe convenient for future extensions, since we can't interfere to Participant model"""
    owner = models.OneToOneField(to=Participant, on_delete=models.CASCADE, )
    megasession = models.ForeignKey(to='MegaSession', on_delete=models.CASCADE, related_name='megaparticipants')
    group = models.ForeignKey(to='MegaGroup',
                              on_delete=models.SET_NULL,
                              related_name='megaparticipants',
                              null=True,
                              blank=True)


class MegaGroup(models.Model):
    """links two random participants together to calculate their payoffs.
    Will it contain the code for actual payoff calculations? Seems logical place for that.
    Megagroup is different from a normal oTree group, because the participants can belong to the different oTree sessions,
    the umbrella is megasession."""
    megasession = models.ForeignKey(to='MegaSession', on_delete=models.CASCADE, related_name='megagroups')
