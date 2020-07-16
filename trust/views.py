from django.views.generic import ListView, View, DetailView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from .models import Decision, Instruction, Player
from django.http import HttpResponse
from io import BytesIO
from datetime import datetime
from .pivot import get_full_data
import pandas as pd
import logging

logger = logging.getLogger(__name__)


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


class PandasExport(View):
    url_name = 'export_pivot'
    display_name = 'Export decisions (Excel)'
    url_pattern = fr'export/wide/csv'
    content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    def get(self, request, *args, **kwargs):
        bytes = BytesIO()
        csv_data = get_full_data()

        if csv_data is not None and not csv_data.empty:
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
        else:
            return HttpResponseRedirect(reverse_lazy('ExportIndex'))


class InstructionCard(DetailView):
    """
    Instruction card
    """
    url_pattern = 'instructions/<participant_code>/<card_number>'
    url_name = 'instruction_card'
    template_name = 'trust/includes/cards/main_card.html'
    model = Instruction
    context_object_name = 'card'

    def get(self, request, *args, **kwargs):
        r = super().get(request, *args, **kwargs)
        self.object.seen += 1
        self.object.save()
        return r

    def get_object(self, queryset=None):
        all_player_cards = Instruction.objects.filter(
            owner=Player.objects.get(participant__code=self.kwargs.get('participant_code')))
        try:
            return all_player_cards.get(page_number=self.kwargs.get('card_number'))
        except  Instruction.DoesNotExist:
            return all_player_cards.get(page_number=1)
