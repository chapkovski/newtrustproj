from django.views.generic import TemplateView, DetailView, ListView, RedirectView
from django.views.generic.edit import CreateView, DeleteView
from .models import MegaSession, MegaParticipant
from django.urls import reverse_lazy
from otree.models import Participant
from django.contrib import messages


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
    success_url = reverse_lazy('mingle_home')

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
        return MingleFormSet(data=post_data, form_kwargs=dict(owner=self.object),
                             queryset=MingleSession.objects.filter(megasession__isnull=True)
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
        return MegaParticipant.objects.filter(megasession=self.get_megasession())


class TurnBackToMegaSession(MegaSessionMixin, RedirectView):
    pattern_name = 'MegaSessionDetail'

    def do_something(self):
        pass

    def get_redirect_url(self, *args, **kwargs):
        self.do_something()
        return super().get_redirect_url(*args, **kwargs)


class CreateGroupsView(TurnBackToMegaSession):
    url_pattern = 'mingle/megasession/creategroups/<int:pk>'
    url_name = 'mega_create_groups'

    def do_something(self):
        m = self.get_megasession()
        m.form_groups()


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
