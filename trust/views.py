from django.views.generic import TemplateView, ListView, View
from django.urls import reverse
from .models import Decision
from django.db.models import Q
import pandas as pd
from django_pandas.io import read_frame
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponse



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




"""
We make a form for locking/unlocking instruction pages here.
"""
from django.views.generic.edit import UpdateView

from django.urls import reverse
from django.http import HttpResponseRedirect



from io import StringIO as IO, BytesIO
from datetime import datetime
from .pivot import get_full_data
import pandas as pd
from django.utils.encoding import smart_str


class PandasExport(View):
    url_name = 'export_pivot'
    display_name = 'Export decisions (Excel)'
    url_pattern = fr'export/wide/csv'
    content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    def get(self, request, *args, **kwargs):
        bytes = BytesIO()
        csv_data = get_full_data()
        xlwriter = pd.ExcelWriter(bytes, engine='xlsxwriter')
        csv_data.to_excel(xlwriter, sheet_name='Sheet1', index=False, header=True)
        xlwriter.save()
        xlwriter.close()
        bytes.seek(0)

        response = HttpResponse(bytes.read(), content_type=self.content_type)
        formatted_date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'decisions_wide_{formatted_date}.xlsx'
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
