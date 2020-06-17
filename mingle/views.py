from django.views.generic import TemplateView, DetailView
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
    # def get(self, request, *args, **kwargs):
    #     # TODO if no free minglesessions - reutrn back with message
    #     if not - just render normally
    #     request, *args, ** kwargs
    def get_formset(self):
        return MingleFormSet(form_kwargs=dict(owner=self.object),
                             queryset=MingleSession.objects.filter(megasession__isnull=True)
                             )

    def get_context_data(self, **kwargs):
        r = super().get_context_data(**kwargs)

        r['formset'] = self.get_formset()
        return r

    def form_valid(self, form):
        self.object = form.save()
        formset = MingleFormSet(self.request.POST, form_kwargs=dict(owner=self.object),
                                queryset=MingleSession.objects.filter(megasession__isnull=True)
                                )
        print(formset.is_valid(), 'VALID??')
        print(formset.errors, 'errors')
        if formset.is_valid():
            formset.save()
        # print(formset.is_valid(), 'VALID??')
        #
        # mingles = form.cleaned_data['mingles']
        # owners = [i.owner for i in mingles]
        # mingles_to_update = mingles.update(megasession=self.object)
        #
        # # we need to get all participants that belong to owner sessions, and create corresposponding
        # # megaparticipants. Should we allow to detach a specific session from megasession? It seems it's
        # # easier just to let them delete megasessions, and thus all megaparticipants and megagroups will be
        # # deleted as well. (In deletion we need to check that payoffs have not been yet formed, and if yes we should
        # # block the deletion. (using pre_delete signal apparently).
        #
        # participants = Participant.objects.filter(session__in=owners)
        # megapars = [MegaParticipant(owner=i, megasession=self.object) for i in participants]
        #
        # MegaParticipant.objects.bulk_create(megapars)
        return HttpResponseRedirect(self.get_success_url())


class MegaSessionDetail(DetailView):
    url_pattern = 'mingle/megasession/detail/<pk>'
    url_name = 'MegaSessionDetail'
    template_name = 'mingle/MegaSessionDetail.html'
    model = MegaSession
    http_method_names = ['get']
    success_url = reverse_lazy('mingle_home')


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
