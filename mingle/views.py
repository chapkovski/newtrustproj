from django.views.generic import TemplateView, DetailView, ListView, RedirectView
from django.views.generic.edit import CreateView, DeleteView
from .models import MegaSession, MegaParticipant, NotEnoughParticipants
from django.urls import reverse_lazy
from otree.models import Participant
from django.contrib import messages
from django.db.models import F, Count, Value, IntegerField, Q, BooleanField, Case, When


def case_builder(field_name):
    return Case(
        When(group__isnull=False, then=f'group__{field_name}'),
        When(pseudogroup__isnull=False, then=f'pseudogroup__{field_name}'),
        default=None,
        output_field=IntegerField()
    )


class MinglerHome(TemplateView):
    """Home page for mingler. Contains links to Create new megasession,
    Edit megasession (basically for detach the attached sessions
    """
    url_pattern = 'mingle/home'
    url_name = 'mingle_home'
    display_name = 'Mingler'
    template_name = 'mingle/MinglerHome.html'

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['megasessions'] = MegaSession.objects.all()
        return c


from .forms import MegaForm, MingleFormSet
from django.http import HttpResponseRedirect
from .models import MingleSession


class CreateNewMegaSession(CreateView):
    """
    Creating new megasession out of unattached minglesessions
    """
    url_pattern = 'mingle/megasession/create'
    url_name = 'CreateNewMegaSession'
    template_name = 'mingle/CreateNewMegasession.html'
    model = MegaSession
    form_class = MegaForm

    # success_url = reverse_lazy('mingle_home')

    def get(self, request, *args, **kwargs):
        q = MingleSession.objects.filter(megasession__isnull=True).exists()
        if not q:
            messages.error(request,
                           """
                           Cannot create new megasession: all sessions are already members of other megasessions! 
                           Either wait till new data is added or delete existing megasessions.
                           """,
                           extra_tags='alert alert-danger')
            return HttpResponseRedirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def get_formset(self, post_data=None):
        filt = Count('owner__trust_player', filter=Q(owner__trust_player__calculable=True))
        q = MingleSession.objects.filter(megasession__isnull=True).annotate(calcs=filt)
        return MingleFormSet(data=post_data, form_kwargs=dict(owner=self.object),
                             queryset=q
                             )

    def get_context_data(self, **kwargs):
        r = super().get_context_data(**kwargs)

        r['formset'] = self.get_formset()
        return r

    def form_valid(self, form):
        self.object = form.save(commit=False)
        formset = self.get_formset(post_data=self.request.POST)

        if formset.is_valid():
            form.save(commit=True)
            formset = self.get_formset(post_data=self.request.POST)
            formset.save()
        else:
            form.add_error(None, "Please select at least one session")
            return self.form_invalid(form)

        return HttpResponseRedirect(self.get_success_url())


class MegaSessionMixin:
    def get_megasession(self):
        pk = self.kwargs.get('pk')
        megasession = MegaSession.objects.get(id=pk)
        return megasession


class MegaSessionDetail(MegaSessionMixin, ListView):
    url_pattern = 'mingle/megasession/detail/<int:pk>'
    url_name = 'MegaSessionDetail'
    template_name = 'mingle/MegaSessionDetail.html'
    context_object_name = 'mparticipants'
    http_method_names = ['get']
    success_url = reverse_lazy('mingle_home')
    paginate_by = 50

    def get_context_data(self, *args, **kwargs):
        r = super().get_context_data(*args, **kwargs)
        r['megasession'] = self.get_megasession()
        return r

    def get_queryset(self):
        return MegaParticipant.objects.filter(megasession=self.get_megasession(),
                                              owner__trust_player__calculable=True). \
            annotate(playerrole=F('owner__trust_player___role'),
                     sender2receiver=case_builder('sender_decision_re_receiver'),
                     receiver2sender=case_builder('receiver_decision_re_sender'),
                     sender_belief=case_builder('sender_belief_re_receiver'),
                     receiver_belief=case_builder('receiver_belief_re_sender'),
                     is_pseudogrouped=Case(
                         When(
                             Q(group__isnull=True) & Q(pseudogroup__isnull=False),
                             then=Value(True)),
                         default=Value(False),
                         output_field=BooleanField())

                     ). \
            order_by('is_pseudogrouped', 'group', '-playerrole')


class TurnBackToMegaSession(MegaSessionMixin, RedirectView):
    pattern_name = 'MegaSessionDetail'

    def do_something(self):
        pass

    def get_redirect_url(self, *args, **kwargs):
        self.do_something()
        return super().get_redirect_url(*args, **kwargs)


class GroupCalculateView(TurnBackToMegaSession):
    url_pattern = 'mingle/megasession/group_and_calculate/<int:pk>'
    url_name = 'mega_group_and_recalculate'

    def get_redirect_url(self, *args, **kwargs):
        m = self.get_megasession()
        try:
            m.form_groups()
            m.calculate_payoffs()
        except NotEnoughParticipants:
            messages.error(self.request, 'Not enough participants: we need at least one sender and one receiver!',
                           extra_tags='alert alert-danger')
        return super().get_redirect_url(*args, **kwargs)


class CalculatePayoffsView(TurnBackToMegaSession):
    url_pattern = 'mingle/megasession/calculatepayoffs/<int:pk>'
    url_name = 'mega_calculate_payoffs'

    def do_something(self):
        m = self.get_megasession()
        m.calculate_payoffs()


class DeleteMegaSession(DeleteView):
    url_pattern = 'mingle/megasession/delete/<pk>'
    url_name = 'DeleteMegaSession'
    template_name = 'mingle/MegaSessionDeleteConfirm.html'
    model = MegaSession
    success_url = reverse_lazy('mingle_home')

    def get(self, request, *args, **kwargs):
        instance = self.get_object(self.get_queryset())
        if not instance.deletable:
            messages.error(request, 'Cannot delete this megasession!', extra_tags='alert alert-danger')
            return HttpResponseRedirect(self.success_url)
        return super().get(self, request, *args, **kwargs)


class MegaSessionStats(DetailView):
    """
    Getting megasession stats per city
    """
    url_pattern = 'mingle/megasession/stats/<int:pk>'
    url_name = 'MegaSessionStats'
    template_name = 'mingle/MegasessionStats.html'
    model = MegaSession
    context_object_name = 'ms'
