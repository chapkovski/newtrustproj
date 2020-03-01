from django.views.generic import TemplateView, ListView
from django.urls import reverse
from .models import SenderDecision
from django.db.models import Q
import pandas as pd
from django_pandas.io import read_frame


class TestListView(ListView):
    url_name = 'test_export'
    display_name = 'Test'
    template_name = 'trust/admin/DecisionList.html'
    url_pattern = r'^export/trust/decisions'

    def get_queryset(self):
        q = SenderDecision.objects.filter(send__isnull=False)

        if q.exists():

            df = read_frame(q, fieldnames=['owner__participant__code','city__code', 'send'])
            # df = pd.DataFrame(q)
            # print('JOPA', df.columns)
            a = df.pivot( index='owner__participant__code',columns='city__code', values=['send', ])

            # for i in a:
            #     print(a.)
            # d = pd.DataFrame(a)
            # print('JOPA', d.size, d.ndim, d.shape)
            print("JOPA", a.columns)
            return {'records':a.to_records(), "columns": a.columns}
        else:
            return 'Nothing here'
