from otree.models import Participant
from otree.models_concrete import PageCompletion
import pandas as pd

p = Participant.objects.all()
pages = ['CQ1', 'CQ2', 'SenderDecisionP', 'SenderBeliefP', 'ReturnDecisionP', 'ReturnerBeliefP', 'Average2', 'Average3',
         'Motivation', ]
q = PageCompletion.objects.filter(page_name__in=pages)
ps = q.values('participant__code', 'page_name', 'seconds_on_page')

df = pd.DataFrame(list(ps))

table = pd.pivot_table(df, values='seconds_on_page', index=['participant__code'],
                       columns=['page_name'])
# table.columns = ['_'.join(col).strip() for col in table.columns.values]
print(table)

for i in q:
    print(i.page_name, i.seconds_on_page, i.participant.code)
