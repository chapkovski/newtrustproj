"""This module is for 'visual' testing - it creates a bunch of data so we can visually
tst the mingler interface.
NOT A PROPER TEST. Proper ones are in test_mingle.py here.
"""
from otree.session import create_session
from trust.models import Player, Decision, Constants
from mingle.models import MegaParticipant, MegaSession
import random
import pandas as pd
import numpy as np
from django.db.models import Count, F, Q
ms = MegaSession.objects.get(id=3)
q = ms.megaparticipants.values(
    city1=F('city__description'),
    role=F('owner__trust_player___role'),
).annotate(
    number=Count('pk')
).order_by('city1')
print(q)