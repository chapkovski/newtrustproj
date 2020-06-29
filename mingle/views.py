from django.views.generic import TemplateView, DetailView, ListView, RedirectView
from django.views.generic.edit import CreateView, DeleteView
from .models import MegaSession, MegaParticipant, NotEnoughParticipants
from django.urls import reverse_lazy
from otree.models import Participant
from django.contrib import messages
from django.db.models import F, Count, Value, IntegerField, Q, BooleanField, Case, When
from django.contrib.auth.mixins import LoginRequiredMixin


def case_builder(field_name):
    return Case(
        When(group__isnull=False, then=f'group__{field_name}'),
        When(pseudogroup__isnull=False, then=f'pseudogroup__{field_name}'),
        default=None,
        output_field=IntegerField()
    )


class MinglerHome(LoginRequiredMixin, TemplateView):
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


class CreateNewMegaSession(LoginRequiredMixin, CreateView):
    """
    Creating new megasession out of unattached minglesessions
    """
    url_pattern = 'mingle/megasession/create'
    url_name = 'CreateNewMegaSession'
    template_name = 'mingle/CreateNewMegasession.html'
    model = MegaSession
    form_class = MegaForm

    def no_mingle_sessions(self):
        messages.error(self.request,
                       """
                       Cannot create new megasession: all sessions are already members of other megasessions! 
                       Either wait till new data is added or delete existing megasessions.
                       """,
                       extra_tags='alert alert-danger')
        return HttpResponseRedirect(reverse_lazy('mingle_home'))

    def get_queryset(self):
        filt = Count('owner__trust_player', filter=Q(owner__trust_player__calculable=True))
        q = MingleSession.objects.filter(megasession__isnull=True).annotate(calcs=filt).\
            exclude(calcs=0)
        return q

    def get(self, request, *args, **kwargs):
        q = self.get_queryset()
        if not q.exists():
            return self.no_mingle_sessions()
        return super().get(request, *args, **kwargs)

    def get_formset(self, post_data=None):
        q = self.get_queryset()
        return MingleFormSet(data=post_data, form_kwargs=dict(owner=self.object),
                             queryset=q
                             )

    def get_context_data(self, **kwargs):
        r = super().get_context_data(**kwargs)

        r['formset'] = self.get_formset()
        return r

    def form_invalid(self, form):
        if not self.get_queryset().exists():
            return self.no_mingle_sessions()
        r = super().form_invalid(form)
        return r

    def form_valid(self, form):
        self.object = form.save(commit=False)
        formset = self.get_formset(post_data=self.request.POST)

        if formset.is_valid():
            form.save(commit=True)
            formset = self.get_formset(post_data=self.request.POST)
            formset.save()
        else:
            for i in formset.non_form_errors():
                form.add_error(None, i)
            return self.form_invalid(form)

        return HttpResponseRedirect(self.get_success_url())


class MegaSessionMixin:
    def get_megasession(self):
        pk = self.kwargs.get('pk')
        megasession = MegaSession.objects.get(id=pk)
        return megasession

    def nonexistent(self):
        try:
            self.get_megasession()
        except             MegaSession.DoesNotExist:
            messages.error(self.request,
                           """
                          Sorry, this megasession no longer exists
                           """,
                           extra_tags='alert alert-danger')
            return HttpResponseRedirect(reverse_lazy('mingle_home'))
        return False

    def get(self, request, *args, **kwargs):
        existence = self.nonexistent()
        return existence or super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        existence = self.nonexistent()
        return existence or super().post(request, *args, **kwargs)


class MegaSessionDetail(LoginRequiredMixin, MegaSessionMixin, ListView):
    url_pattern = 'mingle/megasession/detail/<int:pk>'
    url_name = 'MegaSessionDetail'
    template_name = 'mingle/MegaSessionDetail.html'
    context_object_name = 'mparticipants'
    http_method_names = ['get']
    success_url = reverse_lazy('mingle_home')
    paginate_by = 50

    def get(self, request, *args, **kwargs):
        try:
            self.get_megasession()
        except             MegaSession.DoesNotExist:
            messages.error(request,
                           """
                          Sorry, this megasession no longer exists
                           """,
                           extra_tags='alert alert-danger')
            return HttpResponseRedirect(reverse_lazy('mingle_home'))
        return super().get(request, *args, **kwargs)

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


class GroupCalculateView(LoginRequiredMixin, TurnBackToMegaSession):
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


class CalculatePayoffsView(LoginRequiredMixin, TurnBackToMegaSession):
    url_pattern = 'mingle/megasession/calculatepayoffs/<int:pk>'
    url_name = 'mega_calculate_payoffs'

    def do_something(self):
        m = self.get_megasession()
        m.calculate_payoffs()


class DeleteMegaSession(LoginRequiredMixin, MegaSessionMixin, DeleteView):
    url_pattern = 'mingle/megasession/delete/<pk>'
    url_name = 'DeleteMegaSession'
    template_name = 'mingle/MegaSessionDeleteConfirm.html'
    model = MegaSession
    success_url = reverse_lazy('mingle_home')
    # TODO: later on control for non-deletion!
    # def get(self, request, *args, **kwargs):
    #     instance = self.get_object(self.get_queryset())
    #     if not instance.deletable:
    #         messages.error(request, 'Cannot delete this megasession!', extra_tags='alert alert-danger')
    #         return HttpResponseRedirect(self.success_url)
    #     return super().get(self, request, *args, **kwargs)


class MegaSessionStats(LoginRequiredMixin, MegaSessionMixin, DetailView):
    """
    Getting megasession stats per city
    """
    url_pattern = 'mingle/megasession/stats/<int:pk>'
    url_name = 'MegaSessionStats'
    template_name = 'mingle/MegaSessionStats.html'
    model = MegaSession
    context_object_name = 'ms'

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['num_parts'] = MegaParticipant.objects.filter(megasession=self.object,
                                                        owner__trust_player__calculable=True).count()
        c['total_payoff'] = self.object.total_payoff()
        c['pseudogrouped'] = self.object.megaparticipants.filter(group__isnull=True,
                                                                 pseudogroup__isnull=False).count()
        return c


class MegaParticipantDetail(DetailView):
    """
    Resulting page for a participant
    """
    url_pattern = 'mingle/participant/results/<code>'
    url_name = 'mega_participant_results'
    template_name = 'mingle/MegaParticipantResults.html'
    model = MegaParticipant
    context_object_name = 'p'

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        if not self.get_owner():
            c['message'] = 'Sorry, the code is wrong'
            return c
        obj = self.get_object()
        if not obj or not (obj.group or obj.pseudogroup):
            c['message'] = 'Sorry, no results yet.'
            return c
        if obj.group:
            decision = obj.decision(pseudo=False)
            belief = obj.belief(pseudo=False)
            other_decision = obj.other.decision(pseudo=False)
        elif obj.pseudogroup and not obj.group:
            decision = obj.decision(pseudo=True)
            belief = obj.belief(pseudo=True)
            other_decision = obj.other.decision(pseudo=True)
        c['decision'] = decision
        c['belief'] = belief
        c['other_decision'] = other_decision

        return c

    def get_template_names(self):
        obj = self.get_object()
        if obj and obj.payoff_calculated:
            return [self.template_name]

        return ['mingle/NoResultsYet.html']

    def get_owner(self):
        try:
            return Participant.objects.get(code=self.kwargs.get('code'))
        except Participant.DoesNotExist:
            pass

    def get_object(self, queryset=None):
        try:
            m = MegaParticipant.objects.get(owner__code=self.kwargs.get('code'))
            return m
        except MegaParticipant.DoesNotExist:
            pass
