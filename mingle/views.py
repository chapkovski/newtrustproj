from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .models import MegaSession, MegaParticipant
from django.urls import reverse_lazy
from otree.models import Participant


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
        c['megasessions'] = []
        return c


from .forms import MegaForm
from django.http import HttpResponseRedirect


class CreateNewMegaSession(CreateView):
    """Home page for mingler. Contains links to Create new megasession,
    Edit megasession (basically for detach the attached sessions
    """
    url_pattern = 'mingle/megasession/create'
    url_name = 'CreateNewMegaSession'
    template_name = 'mingle/CreateNewMegasession.html'
    model = MegaSession
    form_class = MegaForm
    success_url = reverse_lazy('mingle_home')

    def form_valid(self, form):
        self.object = form.save()
        mingles = form.cleaned_data['mingles']
        owners = [i.owner for i in mingles]
        mingles_to_update = mingles.update(megasession=self.object)

        # we need to get all participants that belong to owner sessions, and create corresposponding
        # megaparticipants. Should we allow to detach a specific session from megasession? It seems it's
        # easier just to let them delete megasessions, and thus all megaparticipants and megagroups will be
        # deleted as well. (In deletion we need to check that payoffs have not been yet formed, and if yes we should
        # block the deletion. (using pre_delete signal apparently).

        participants = Participant.objects.filter(session__in=owners)
        megapars = [MegaParticipant(owner=i, megasession=self.object) for i in participants]

        MegaParticipant.objects.bulk_create(megapars)
        return HttpResponseRedirect(self.get_success_url())


