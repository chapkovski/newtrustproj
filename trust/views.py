from django.views.generic import TemplateView, ListView
from django.urls import reverse
from .models import Decision
from django.db.models import Q
import pandas as pd
from django_pandas.io import read_frame
from django.http import HttpResponse
from django.template import loader


class PaginatedListView(ListView):
    navbar_active_tag = None
    export_link_name = None
    export_activated = None
    title = ''
    context_object_name = 'statements'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['title'] = self.title
        c['nbar'] = self.navbar_active_tag
        curpage_num = c['page_obj'].number
        paginator = c['paginator']
        epsilon = 3
        c['allowed_range'] = range(max(1, curpage_num - epsilon), min(curpage_num + epsilon, paginator.num_pages) + 1)
        if self.export_link_name:
            c['export_link'] = self.export_link_name
        c['export_activated'] = self.export_activated or False
        return c


class DecisionListView(PaginatedListView):
    url_name = 'decisions'
    display_name = 'Decisions - long format'
    template_name = 'trust/admin/DecisionList.html'
    url_pattern = r'^export/trust/decisions/long'

    context_object_name = 'decisions'
    paginate_by = 50
    navbar_active_tag = 'decisions'
    export_activated = True
    export_link_name = 'decisions_long_csv'
    model = Decision
    queryset = Decision.objects.filter(answer__isnull=False)


class ExportToCSV(ListView):
    content_type = 'text/csv'
    filename = None

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type=self.content_type)
        response['Content-Disposition'] = f'attachment; filename="{self.filename}"'
        t = loader.get_template(self.template_name)
        c = {
            'data': self.get_queryset(),
        }
        response.write(t.render(c))
        return response

from django_pivot.pivot import pivot
class DecisionPivotView(ListView):
    url_name = 'decisions_wide'
    display_name = 'Decisions - wide format'
    template_name = 'trust/admin/DecisionWideList.html'
    url_pattern = r'^export/trust/decisions/wide'
    pagination_class = None
    paginate_by = None
    context_object_name = 'decisions'

    navbar_active_tag = 'decisions'
    export_activated = False
    model = Decision
    queryset = Decision.objects.filter(answer__isnull=False)

    def get_queryset(self):
        q = self.queryset


        if q.exists():
            pivot_table = pivot(q, ['owner__participant__code', 'decision_type'], 'city__code', 'answer')
            print('PIVAOT!', pivot_table)
            fields = pivot_table.first().keys()
            print("NAMES::", fields)
            return pivot_table

class DecisionLongCSVExport(ExportToCSV):
    filename = 'decisions_long.csv'
    template_name = 'trust/admin/csv/decisions_long.csv'
    queryset = Decision.objects.filter(answer__isnull=False)
    url_name = 'decisions_long_csv'
    url_pattern = r'^export/trust/decisions/long/csv$'


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
