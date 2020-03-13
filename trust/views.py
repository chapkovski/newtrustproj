from django.views.generic import TemplateView, ListView, View
from django.urls import reverse
from .models import Decision
from django.db.models import Q
import pandas as pd
from django_pandas.io import read_frame
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponse
from .resources import DecisionResource


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
        person_resource = DecisionResource()
        dataset = person_resource.export(self.queryset)
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{self.filename}"'
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
            pivot_table = pivot(q, ['owner__participant__code', 'owner__city', 'decision_type'], 'city__description',
                                'answer')
            return pivot_table


class DecisionLongCSVExport(ExportToCSV):
    filename = 'decisions_long.xls'
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


from io import StringIO as IO
from otree.models import Participant
import pandas as pd
from trust.models import Decision
from datetime import datetime
from questionnaire.models import Player as QPlayer
from django.utils import timezone


from .pivot import get_full_data
class PandasExport(View):
    url_name = 'export_pivot'
    display_name = 'Export decisions (CSV)'
    url_pattern = fr'export/wide/csv'
    content_type = 'text/csv'

    def get(self, request, *args, **kwargs):
        # q = Decision.objects.all()
        # df = pd.DataFrame(list(q.values('city__code', 'decision_type', 'owner__participant__code', 'answer')))
        # table = pd.pivot_table(df, values='answer', index=['owner__participant__code'],
        #                        columns=['decision_type', 'city__code'])
        # table.columns = ['_'.join(col).strip() for col in table.columns.values]
        # qsdata = QPlayer.objects.all()
        # dfq = pd.DataFrame(list(qsdata.values()))

        csv_file = IO()

        csv_data = get_full_data()
        csv_data.to_csv(csv_file, index=False, header=True)
        csv_file.seek(0)
        response = HttpResponse(csv_file.read(), content_type=self.content_type)
        formatted_date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'decisions_wide_{formatted_date}.csv'
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
