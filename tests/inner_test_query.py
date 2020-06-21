"""This module is for 'visual' testing - it creates a bunch of data so we can visually
tst the mingler interface.
NOT A PROPER TEST. Proper ones are in test_mingle.py here.
"""
from otree.session import create_session
from trust.models import Player, Decision, Constants
from mingle.models import MegaParticipant
import random
import pandas as pd
import numpy as np
from django.db.models import Count, F, Q

data = MegaParticipant.objects.filter(group__isnull=False).filter(
    Q(group__megaparticipants__lt=F('pk')) | Q(group__megaparticipants__gt=F('pk'))
).values(
    city1=F('city__description'),
    city2=F('group__megaparticipants__city__description')
).annotate(
    number=Count('pk')
).order_by('city1', 'city2')

df = pd.DataFrame(data)
df['whaterver'] = df.groupby('city1')['number'].transform('sum')
df['perc'] = df['number'] / df['whaterver']
a = df.groupby('city1')['perc'].agg([np.min, np.max, np.median])
print(a)
pd.options.display.float_format = '{0:.0%}'.format
table = pd.pivot_table(df, values='perc', index=['city1'],
                       columns=['city2'])
print(table)
