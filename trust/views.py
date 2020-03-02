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

            df = read_frame(q, fieldnames=['owner__participant__code', 'city__code', 'send'])

            a = df.pivot(index='owner__participant__code', columns='city__code', values=['send', ])

            return {'records': a.to_records(), "columns": a.columns}
        else:
            return 'Nothing here'


"""
We make a form for locking/unlocking instruction pages here.
"""
from django.views.generic.edit import UpdateView
from .models import Blocker
from django.urls import reverse
from django.http import HttpResponseRedirect


class AllowInstructions(UpdateView):
    url_pattern = r'^change_lock/(?P<pk>\d+)$'
    url_name = 'change_lock'
    http_method_names = ['post']
    model = Blocker

    def get_success_url(self):
        obj = self.get_object()
        return reverse('AdminReport', args=[obj.session.code])

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.locked = not obj.locked
        obj.save()
        return HttpResponseRedirect(self.get_success_url())
