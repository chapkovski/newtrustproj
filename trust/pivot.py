def report():
    import pandas as pd


#     from trust.models import Decision
#     import tempfile
#     q = Decision.objects.filter(answer__isnull=False)
#     df = pd.DataFrame(list(q.values('city__code', 'decision_type', 'owner__participant__code', 'answer')))
#     table = pd.pivot_table(df, values='answer', index=['owner__participant__code'],
#                            columns=['decision_type', 'city__code'])
#     table.reset_index(inplace=True)
#     table.columns = ['_'.join(col).strip() for col in table.columns.values]
#     # print(table.columns)
#
#     return table.to_csv( index=False, header=True)
#
#
# if __name__ == '__main__' or __name__ == 'django.core.management.commands.shell':
#     report()

from trust.models import Decision, Player
from otree.models import Participant
import random

print('WAS', Decision.objects.all().count())
partslist = []
playerslist = []
d = Decision.objects.first()
PP = Participant.objects.first()
P = Player.objects.first()
from uuid import uuid4

for i in range(1000):

    part = PP
    part.pk = None
    part.code = str(uuid4())
    part.save()
    print("NEW COEDE",part.code,i)
    partslist.append(part)
# Participant.objects.bulk_create(partslist)
for partici in partslist:
    newp = P
    newp.pk = None
    newp.save()
    print(i)
    playerslist.append(newp)
# Player.objects.bulk_create(playerslist)
l = []
for player in playerslist:
    p = d
    p.pk = None
    p.owner = player
    l.append(p)
Decision.objects.bulk_create(l)
print('IS', Decision.objects.all().count())
