"""
testing how the group info retrieval works

"""
from otree.session import create_session
from trust.models import Player, Decision, Constants
from mingle.models import MegaParticipant, MegaSession, MegaGroup
import random
import pandas as pd
import numpy as np

from django.db.models import Count, F, Q

g = MegaGroup.objects.get(id=1)
gq = MegaGroup.objects.filter(id=1).filter(megaparticipants__owner__trust_player___role='sender').\
    annotate(senderrole=F('megaparticipants__owner__trust_player___role'),
             receiverrrole=F('megaparticipants__owner__trust_player___role'),)
for i in gq:
    print(i.senderrole)

# How it would look like if group would have sender and receiver fields
# gq = MegaGroup.objects.filter(id=1).\
#     annotate(sender_towards_receiver=)
