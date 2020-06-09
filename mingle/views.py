from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .models import MegaSession
from django.urls import reverse_lazy


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
        mingles =  form.cleaned_data['mingles']
        mingles.update(wrapper=self.object)
        return HttpResponseRedirect(self.get_success_url())




