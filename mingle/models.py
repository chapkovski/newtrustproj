"""
Contains models for mingling sessions into larger megasessions, plus some 1to1 to Participant model
"""
from otree.models import Participant, Session
from django.db import models


class MingleSession(models.Model):
    """1to1 to prevent double mingling"""
    owner = models.OneToOneField(to=Session, on_delete=models.CASCADE, related_name='minglesession')
    wrapper = models.ForeignKey(to='MegaSession', on_delete=models.CASCADE, related_name='minglesessions',
                                null=True, blank=True)


class MegaSession(models.Model):
    """Container for all sessions beloning to one mega"""
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return f'Wrapper for {self.minglesessions.all().count()}'


class MegaParticipant(models.Model):
    """1to1 link to participant for freezing those whose payoffs were calculated.
    Not really necessary but maybe convenient for future extensions, since we can't interfere to Participant model"""
    owner = models.OneToOneField(to=Participant, on_delete=models.CASCADE, )
    wrapper = models.ForeignKey(to='MegaSession', on_delete=models.CASCADE, related_name='megaparticipants')
    group = models.ForeignKey(to='MegaGroup',
                              on_delete=models.CASCADE,
                              related_name='megaparticipants',
                              null=True,
                              blank=True)


class MegaGroup(models.Model):
    """links two random participants together to calculate their payoffs.
    Will it contain the code for actual payoff calculations? Seems logical place for that"""
